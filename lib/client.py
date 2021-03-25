import sys
import time
import datetime

import asyncio
from asyncio.exceptions import TimeoutError

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

import logging
import logging.handlers
from logging.handlers import SysLogHandler
from logging import Formatter


from typing import List, Optional

# from lib.exceptions import RateLimited, UserNotFound

class BaseClient:
    def __init__(
        self,
        *,
        host,
        path,
        verbose,
        port="",
        is_ssl=True,
        timeout=5,
        retries=6,
        retry_wait=1,
        max_timeout=300,
        max_retry_wait=300,
        rate_limit_countdown=1,
        rate_limit_in_effect=False,
        countdown=0,
        filo_queue_wait=80,
        filo_queue_step=10,
    ):
        self.is_ssl = is_ssl
        self.host = host
        self.port = port
        self.path = path
        self.verbose = verbose
        self.timeout = timeout
        self.retries = retries
        self.retry_wait = retry_wait
        self.scheme = "https" if self.is_ssl else "http"
        self.url = f"{self.scheme}://{self.host}:{self.port}{self.path}"
        self.logger = logging.getLogger("aiohttp.internal")
        self.logger.setLevel(logging.DEBUG)
        self.handler = SysLogHandler(facility=SysLogHandler.LOG_DAEMON, address='/dev/log')
        self.logger.addHandler(self.handler)
        self.log_format = '[%(levelname)s] %(filename)s:%(funcName)s:%(lineno)d \"%(message)s\"'
        self.handler.setFormatter(Formatter(fmt=self.log_format))
        self.max_timeout = max_timeout
        self.max_retry_wait = max_retry_wait
        self.countdown = countdown
        self.filo_queue_wait = (retries + 1) * filo_queue_step
        self.filo_queue_step = filo_queue_step
        self.rate_limit_in_effect = rate_limit_in_effect

        """
        Calculate First in Last out queing when RATE LIMITING ACTIVE
        When many githuggers are active, ultimately, they may be rate
        limited. So to keep it fair, the most tenacious githuggers will win. 
        First in Last Out means:
        A countdown timer is extablished when rate limiting occurs, this
        is normally one hour the moment rate limiting begins. When countdown
        reaches zero, everyone races to grab limited resources, but...
        On the 1st try, an extra 60 seconds TAX is added to the countdown
        On the 2nd try, an extra 50 seconds TAX is added to the countdown
        On the 6th try, an extra  0 seconds TAX is added to the countdown
        """

    async def retry_after_wait(self, err, func, ):
        print(f"Rate-Limiting? {self.rate_limit_in_effect}")
        if self.retries > 0:
            if self.rate_limit_in_effect:
                print(f"Non LILO queuing { self.countdown}")
                self.countdown = self.countdown +  ( self.retries * self.filo_queue_step )
                msg = f"Sleeping the Rate Limit for {self.countdown}sec. {self.retries} retries remaining"
                self.logger.warning(msg)
                print(f"WAITING! { self.countdown}")
                await asyncio.sleep(self.countdown)
                self.retries = self.retries - 1
                return await func()
            else:
                msg = f"Sleeping potential congestion error {self.retry_wait}sec. {self.retries} retries remaining"
                self.logger.warning(msg)
                await asyncio.sleep(self.retry_wait)
                self.retries = self.retries - 1
                self.retry_wait = min(self.retry_wait * 2, self.max_retry_wait)
                return await func()
        else:
            msg = f"Retries exhausted"
            self.logger.error(msg)
            return (err, None)
    async def get_data(self):
        msg = f"Fetching data from {self.url}"
        self.logger.info(msg)
        ct = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=ct) as session:
            try:
                async with session.get(self.url) as resp:
                    data = await resp.json()
                    hed = resp.headers
                    self.countdown =  int(hed['X-RateLimit-Reset']) - int(time.time())
                    if (self.verbose):
                        print(f"DATA    = {data}\n")
                        print(f"HEADERS = {hed}\n")
                        print(f"Total Limit:        {hed['X-RateLimit-Limit']}")
                        print(f"Remaining:          {hed['X-RateLimit-Remaining']}")
                        print(f"Countdown to reset: {self.countdown}")
                    if isinstance(data, dict):
                        if int(hed['X-RateLimit-Remaining']) <= 0:
                            self.rate_limit_in_effect = True
                            err="RateLimting in effect"
                            return await self.retry_after_wait(err, self.get_data)
                        if (resp.status == 404 ):
                            err = f"{resp.status} github user \"{self.path}\" does not exist"
                            return (err, data)
#                            raise UserNotFound(self, f"YOU DON'T EXIST!!!") 
                    return (None, data)
            except ClientConnectorError as err:
                self.logger.error(err)
                return await self.retry_after_wait(self, err, self.get_data)
            except TimeoutError as err:
                self.timeout = self.timeout * 2
                self.logger.error(
                    f"Request timed out. Retrying with {self.timeout}s timeout")
                return await self.retry_after_wait(err, self.get_data)
            except Exception as err:
                self.logger.error(err)
                return (err, None)
