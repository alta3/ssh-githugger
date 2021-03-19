import sys
import time

import asyncio
from asyncio.exceptions import TimeoutError

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

import logging

from typing import List, Optional

from lib.exceptions import RateLimited, UserNotFound

class BaseClient:
    def __init__(
        self,
        *,
        host,
        path,
        port="",
        is_ssl=True,
        timeout=5,
        retries=6,
        retry_wait=1,
        max_timeout=300,
        max_retry_wait=300,
    ):
        self.is_ssl = is_ssl
        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout
        self.retries = retries
        self.retry_wait = retry_wait
        self.scheme = "https" if self.is_ssl else "http"
        self.url = f"{self.scheme}://{self.host}:{self.port}{self.path}"
        self.logger = logging.getLogger("aiohttp.internal")
        self.max_timeout = max_timeout
        self.max_retry_wait = max_retry_wait

    async def retry_after_wait(self, err, func):
        if self.retries > 0:

            msg = f"Sleeping {self.retry_wait}s. {self.retries} retries remaining"
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
                    print(f"data = {data}\n")
                    # TODO - Only output headers on debug flag from parse_args()
                    print(f"headers = {hed}")
                    print(f"Total Limit:        {hed['X-RateLimit-Limit']}")
                    print(f"Remaining:          {hed['X-RateLimit-Remaining']}")
                    print(f"Reset Time (Epoch): {hed['X-RateLimit-Reset']}")
                    reset_date = time.gmtime(int(hed['X-RateLimit-Reset']))
                    reset_time = time.strftime("%Y-%m-%d %H:%M:%S", reset_date)
                    print(f"Reset Time (GMT):   {reset_time}")
                    if isinstance(data, dict):
                        if int(hed['X-RateLimit-Remaining']) <= 0:
                            raise RateLimited(self.url, f"You have {hed['X-RateLimit-Remaining']} requests remaining. This will be reset at {reset_time}. {data['message']}") 
                        if not data.get("id") and not data.get("key"):
                            raise UserNotFound(self.path, f"YOU DON'T EXIST!!!") 
                    return (None, data)

            except RateLimited as err:
                self.logger.error(err)
                return await self.retry_after_wait(err, self.get_data)

            except ClientConnectorError as err:
                self.logger.error(err)
                return await self.retry_after_wait(err, self.get_data)

            except TimeoutError as err:
                self.timeout = self.timeout * 2
                self.logger.error(
                    f"Request timed out. Retrying with {self.timeout}s timeout"
                )
                return await self.retry_after_wait(err, self.get_data)

            except Exception as err:
                self.logger.error(err)
                return (err, None)
