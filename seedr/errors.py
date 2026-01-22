class InvalidLogin(Exception):
    """Raised when the username and password combination is invalid."""
    pass


class InvalidToken(Exception):
    """Raised when the access token is invalid."""
    pass


class LoginRequired(Exception):
    """Raised when no login credentials are provided."""
    pass


class TokenExpired(Exception):
    """Raised when the access token has expired."""
    pass

