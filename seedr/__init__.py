from .api import SeedrAPI

class InvalidLogin(Exception):
    pass

class InvalidToken(Exception):
    pass

class LoginRequired(Exception):
    pass

class TokenExpired(Exception):
    pass