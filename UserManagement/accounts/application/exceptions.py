class DecodeTokenError(Exception):
    """Exception raised when the JWT token is invalid."""
    pass


class ExpiredTokenError(Exception):
    """Exception raised when the JWT token has expired."""
    pass
