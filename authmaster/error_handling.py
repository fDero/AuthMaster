from __init__ import app
from http import HTTPStatus
from flask import jsonify
from exceptions import *


def return_error_response(message, error_code):
    return jsonify({
        "status": "error",
        "message": message,
        "error-code": error_code
    }), error_code


@app.errorhandler(MissingOAuthTokenException)
def handle_missing_oauth_token(error):
    error_code = HTTPStatus.UNPROCESSED_ENTITY
    return return_error_response(str(error), error_code)


@app.errorhandler(InvalidOAuthTokenException)
def handle_invalid_oauth_token(error):
    error_code = HTTPStatus.UNAUTHORIZED
    return return_error_response(str(error), error_code)


@app.errorhandler(AccountAlreadyExistsException)
def handle_account_already_exists(error):
    error_code = HTTPStatus.CONFLICT
    return return_error_response(str(error), error_code)


@app.errorhandler(DatabaseErrorException)
def handle_database_error(error):
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return return_error_response(str(error), error_code)


@app.errorhandler(MissingRegistrationDataException)
def handle_missing_registration_data(error):
    error_code = HTTPStatus.BAD_REQUEST
    return return_error_response(str(error), error_code)


@app.errorhandler(SmtpConnectionException)
def handle_smtp_connection_error(error):
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return return_error_response(str(error), error_code)


@app.errorhandler(AccountAlreadyVerifiedException)
def handle_account_already_verified(error):
    error_code = HTTPStatus.NOT_MODIFIED
    return return_error_response(str(error), error_code)


@app.errorhandler(TooManyVerificationAttemptsException)
def handle_too_many_verification_attempts(error):
    error_code = HTTPStatus.TOO_MANY_REQUESTS
    return return_error_response(str(error), error_code)


@app.errorhandler(VerificationAttemptFailedException)
def handle_verification_attempt_failed(error):
    error_code = HTTPStatus.UNAUTHORIZED
    return return_error_response(str(error), error_code)


@app.errorhandler(NoAccountToVerifyException)
def handle_no_account_to_verify(error):
    error_code = HTTPStatus.NOT_FOUND
    return return_error_response(str(error), error_code)


@app.errorhandler(NoAccountToLoginException)
def handle_no_account_to_login(error):
    error_code = HTTPStatus.NOT_FOUND
    return return_error_response(str(error), error_code)


@app.errorhandler(IncorrectPasswordException)
def handle_incorrect_password(error):
    error_code = HTTPStatus.UNAUTHORIZED
    return return_error_response(str(error), error_code)


@app.errorhandler(AccountNotManagedByAuthmaster)
def handle_account_not_managed_by_authmaster(error):
    error_code = HTTPStatus.LOCKED
    return return_error_response(str(error), error_code)


@app.errorhandler(MissingLoginDataException)
def handle_missing_login_data(error):
    error_code = HTTPStatus.BAD_REQUEST
    return return_error_response(str(error), error_code)


@app.errorhandler(InvalidEncryptionAlgorithmException)
def handle_invalid_encryption_algorithm(error):
    error_code = HTTPStatus.BAD_REQUEST
    return return_error_response(str(error), error_code)