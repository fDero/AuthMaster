from exceptions import *
from http import HTTPStatus


def ensure_account_to_verify_was_found(account: dict):
    if not account or "_id" not in account:
        raise NoAccountToVerifyException()


def ensure_account_is_not_yet_verified(account: dict):
    if account['state']['status'] != 'unverified':
        raise AccountAlreadyVerifiedException()


def ensure_validation_request_fields_ok(email : str, otp : str):
    if not email or not otp:
        raise MissingRegistrationDataException()


def ensure_registration_request_fields_ok(data: dict):
    email = data.get('email')
    uname = data.get('username')
    passw = data.get('password')
    if not email or not uname or not passw:
        raise MissingRegistrationDataException()


def ensure_google_oauth_token_is_present(data):
    try:
        data.get('X-OAuth-Token')
    except Exception:
        raise MissingOAuthTokenException()


def ensure_google_oauth_token_is_validated(status_code: int):
    if status_code != HTTPStatus.OK:
        raise InvalidOAuthTokenException()
