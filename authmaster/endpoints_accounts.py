from __init__ import *
from flask import jsonify, current_app
from flask import request as flask_incoming_request
from commons import *
from persistence import *
from responses import *
from validation import *
from mailing import *
from exceptions import *


@app.route('/v1/accounts/register/init', methods=['POST'])
def authmaster_register():
    data = flask_incoming_request.get_json()
    ensure_registration_request_fields_ok(data)
    requested_algo = parse_requested_encryption_algo(flask_incoming_request)
    account = register_with_authmaster(
        current_app.config['MONGODB'],
        current_app.config['OWNER'],
        requested_algo,
        data.get('email'), 
        data.get('username'), 
        data.get('password')
    )
    send_verification_email(
        current_app.config['SMTP'],
        account
    )
    email = data.get('email')
    return response_account_registration_init_success(email)


@app.route('/v1/accounts/register/retry', methods=['POST'])
def authmaster_register():
    data = flask_incoming_request.get_json()
    ensure_registration_request_fields_ok(data)
    account = find_account_in_database(current_app.config['MONGODB'], data)
    ensure_account_to_verify_was_found(account)
    ensure_account_is_not_yet_verified(account)
    send_verification_email(
        current_app.config['SMTP'],
        account
    )
    email = data.get('email')
    return response_account_registration_init_success(email)


@app.route('/v1/accounts/register/verify', methods=['POST'])
def authmaster_verify() -> Response:
    data = flask_incoming_request.get_json()
    email = data.get('email')
    otp = data.get('verification-code')
    mongodb = current_app.config['MONGODB']
    ensure_validation_request_fields_ok(email, otp)
    account = mongodb.find_one({'email': email})
    ensure_account_to_verify_was_found(account)
    ensure_account_is_not_yet_verified(account)
    perform_otp_verification_and_update(mongodb, account, otp)
    jwt_secret = current_app.config['JWT_SECRET']
    jwt_token = create_jwt_token(account, jwt_secret, timedelta(days=1))
    return response_access_garanted_success_response(
        account, jwt_token
    )


@app.route('/v1/accounts/login', methods=['POST'])
def authmaster_login() -> Response:
    data = flask_incoming_request.get_json()
    password = data.get('password')
    ensure_login_request_fields_ok(data)
    mongodb = current_app.config['MONGODB']
    account = find_account_in_database(mongodb, data)
    ensure_owner_is_correct(account, current_app.config['OWNER'])
    ensure_account_to_login_was_found(account)
    ensure_password_is_correct(account, password)
    jwt_secret = current_app.config['JWT_SECRET']
    jwt_token = create_jwt_token(account, jwt_secret, timedelta(days=1))
    return response_account_login_success_response(
        account, jwt_token
    )