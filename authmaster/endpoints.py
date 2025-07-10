from __init__ import *
from flask import jsonify, current_app
from flask import request as flask_incoming_request
from http import HTTPStatus
from persistence import *
from mailing import *
from exceptions import *
import requests


@app.route('/ping', methods=['GET', 'HEAD'])
def ping():
    return jsonify({"message": "ping request recieved correctly"})


@app.route('/accounts/register', methods=['POST'])
def authmaster_register():
    data = flask_incoming_request.get_json()
    email = data.get('email')
    uname = data.get('username')
    passw = data.get('password')
    if not email or not uname or not passw:
        raise MissingRegistrationDataException()
    account = register_with_authmaster(
        current_app.config["MONGODB"], 
        current_app.config["OWNER"], 
        email, 
        uname, 
        passw
    )
    send_verification_email(
        current_app.config["SMTP"], 
        account
    )
    return jsonify({
        "status": "success",
        "message": f"An email has been sent to: {email}"
    }), HTTPStatus.CREATED


@app.route('/accounts/verify', methods=['POST'])
def authmaster_verify():
    data = flask_incoming_request.get_json()
    email = data.get('email')
    otp = data.get('verification-code')
    if not email or not otp:
        raise MissingRegistrationDataException()
    mongodb = current_app.config["MONGODB"]
    account = mongodb.find_one({"email": email})
    if not account:
        raise AccountAlreadyExistsException()
    if account['state']['status'] != 'unverified':
        return jsonify({
            "status": "success",
            "message": "Account already verified"
        }), HTTPStatus.NOT_MODIFIED
    if account['state']['email-otp'] != otp:
        mongodb.update_one(
            {"email": email},
            {"$set": {"state.attempts": account['state']['attempts'] + 1}}
        )
        return jsonify({
            "status": "error",
            "message": "Invalid OTP"
        }), HTTPStatus.UNAUTHORIZED
    mongodb.update_one(
        {"email": email},
        {"$set": {"state.status": "verified"}}
    )
    return jsonify({
        "status": "success",
        "message": f"Account {email} has been verified successfully"
    }), HTTPStatus.OK


@app.route('/oauth/google', methods=['POST'])
def oauth_google():
    data = flask_incoming_request.get_json()
    token = data.get('oauth-token')
    if not token: 
        raise MissingOAuthTokenException()
    response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != HTTPStatus.OK:
        raise InvalidOAuthTokenException()
    user_info = response.json()
    return jsonify({ 
        "status": "success",
        "user": {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "id": user_info.get("id"),
            "picture": user_info.get("picture")
        }
    }), HTTPStatus.OK
