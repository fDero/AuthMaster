from exceptions import *
from persistence import *
from http import HTTPStatus


def ensure_account_to_verify_was_found(account: dict):
    if not account or "_id" not in account:
        raise NoAccountToVerifyException()


def ensure_account_is_not_yet_verified(account: dict):
    if account['state']['status'] != 'unverified':
        raise AccountAlreadyVerifiedException()


def ensure_validation_request_fields_ok(email: str, otp: str):
    if not email or not otp:
        raise MissingRegistrationDataException()


def ensure_registration_request_fields_ok(data: dict):
    email = data.get('email')
    uname = data.get('username')
    passw = data.get('password')
    if not email or not uname or not passw:
        raise MissingRegistrationDataException()


def ensure_login_request_fields_ok(data: dict):
    email = data.get('email')
    uname = data.get('username')
    passw = data.get('password')
    if (not email and not uname) or not passw:
        raise MissingLoginDataException()


def ensure_google_oauth_token_is_present(data: dict):
    try:
        data.get('X-OAuth-Token')
    except Exception:
        raise MissingOAuthTokenException()


def ensure_google_oauth_token_is_validated(status_code: int):
    if status_code != HTTPStatus.OK:
        raise InvalidOAuthTokenException()


def ensure_owner_is_correct(account: dict, authmaster_owner: str):
    if account and account['owner'] != authmaster_owner:
        raise AccountNotManagedByAuthmaster()


def ensure_account_to_login_was_found(account: dict):
    if not account or "_id" not in account:
        raise NoAccountToLoginException()


def ensure_password_is_correct(account: dict, password: str):
    hashed_password = account['passw']['hash']
    salt = account['passw']['salt']
    candidate_password_object = get_hashed_password_object(salt, password)
    candidate_hashed_password = candidate_password_object['hash']
    if hashed_password != candidate_hashed_password:
        raise IncorrectPasswordException()