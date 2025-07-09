class MissingOAuthTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid OAuth 2.0 token: missing field or null value")


class InvalidOAuthTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid OAuth 2.0 token: refused from the provider")


class AccountAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("An account with the provided email or username already exists")


class DatabaseErrorException(Exception):
    def __init__(self):
        super().__init__("An error has occurred while trying to query from the database")