class MissingOAuthTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid OAuth 2.0 token: missing field or null value")


class InvalidOAuthTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid OAuth 2.0 token: refused from the provider")