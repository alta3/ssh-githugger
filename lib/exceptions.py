import sys

class Error(Exception):
    pass


class UserNotFound(Error):
    """Exception raised when a user is not found.
    
    Attributes:
        user -- the user that could not be found
        message -- explanaton of the error
    """
    def  __init__(self, user, message):
        self.user = user 
        self.message = message  
        print(
        f"""
        ERROR: UserNotFound
        USER: The user ({self.user}) could not be found. 
        MSG: Please check if the user exists, and verify the spelling.
        {self.message}
        """,
        file=sys.stderr,
        )
        exit(1)


class RateLimited(Error):
    """Exception raised for going over rate limits.

    Attributes:
        url -- url that caused the rate to be exceeded
        message -- explanation of the error
    """        
    def  __init__(self, url, message):
        self.url = url 
        self.message = message  
        print(
        f"""
        YOU JUST GOT RATE LIMITED!
        ERROR: RateLimited
        FROM: {self.url}
        MSG: {self.message}
        """,
        file=sys.stderr,
        )
        exit(1)

