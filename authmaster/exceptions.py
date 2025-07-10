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


class MissingRegistrationDataException(Exception):
    def __init__(self):
        super().__init__("Missing registration data: email, username, or password is not provided")


class SmtpConnectionException(Exception):
    def __init__(self, message: str):
        super().__init__(f"An error has occurred while trying to send an email: {message}")


class AccountAlreadyVerifiedException(Exception):
    def __init__(self):
        super().__init__("The account is already verified, no further action is needed")


class TooManyVerificationAttemptsException(Exception):
    def __init__(self):
        super().__init__("Too many verification attempts, the account has been removed")


class VerificationAttemptFailedException(Exception):
    def __init__(self):
        super().__init__("Verification attempt failed, please try again with the correct OTP code")


class NoAccountToVerifyException(Exception):
    def __init__(self):
        super().__init__("No account to verify was found, please register first or check your email")