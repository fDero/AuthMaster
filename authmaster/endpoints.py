from __init__ import *
from flask import jsonify, current_app
from flask import request as flask_incoming_request
from persistence import *
from responses import *
from validation import *
from mailing import *
from exceptions import *
import requests


@app.route('/ping', methods=['GET', 'HEAD'])
def ping():
    return jsonify({"message": "ping request recieved correctly"})


@app.route('/v1/oauth/google/validate', methods=['GET', 'HEAD'])
def oauth_google_test() -> Response:
    data = flask_incoming_request.headers
    ensure_google_oauth_token_is_present(data)
    token = data.get('X-OAuth-Token')
    response = requests.get(
        GOOGLE_USERINFO_ENDPOINT,
        headers={"Authorization": f"Bearer {token}"}
    )
    ensure_google_oauth_token_is_validated(response.status_code)
    user_info = response.json()
    return response_oauth_token_recognized(user_info, "Google")


@app.route('/v1/accounts/register/init', methods=['POST'])
def authmaster_register():
    data = flask_incoming_request.get_json()
    ensure_registration_request_fields_ok(data)
    account = register_with_authmaster(
        current_app.config["MONGODB"], 
        current_app.config["OWNER"], 
        data.get('email'), 
        data.get('username'), 
        data.get('password')
    )
    send_verification_email(
        current_app.config["SMTP"], 
        account
    )
    email = data.get('email')
    return response_account_registration_init_success(email)


@app.route('/v1/accounts/register/verify', methods=['POST'])
def authmaster_verify() -> Response:
    data = flask_incoming_request.get_json()
    email = data.get('email')
    otp = data.get('verification-code')
    mongodb = current_app.config["MONGODB"]
    ensure_validation_request_fields_ok(email, otp)
    account = mongodb.find_one({"email": email})
    ensure_account_to_verify_was_found(account)
    ensure_account_is_not_yet_verified(account)
    perform_otp_verification_and_update(mongodb, account, otp)
    return response_account_verificaton_success_response(
        account, "EXAMPLE_JWT_TOKEN"
    )


@app.route('/v1/accounts/login', methods=['POST'])
def authmaster_login() -> Response:
    data = flask_incoming_request.get_json()
    email = data.get('email')
    password = data.get('password')
    ensure_login_request_fields_ok(data)
    mongodb = current_app.config["MONGODB"]
    account = find_account_in_database(mongodb, data)
    ensure_owner_is_correct(account, current_app.config["OWNER"])
    ensure_account_to_login_was_found(account)
    ensure_password_is_correct(account, password)
    return response_account_login_success_response(
        account, "EXAMPLE_JWT_TOKEN"
    )