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