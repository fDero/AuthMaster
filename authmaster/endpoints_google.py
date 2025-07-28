from __init__ import *
from flask import jsonify, current_app
from flask import request as flask_incoming_request
from commons import *
from persistence import *
from responses import *
from validation import *
from mailing import *
from exceptions import *
import requests


@app.route('/v1/oauth/google/validate', methods=['GET', 'HEAD'])
def oauth_google_validate() -> Response:
    data = flask_incoming_request.headers
    ensure_google_oauth_token_is_present(data)
    token = data.get('X-OAuth-Token')
    response = requests.get(
        GOOGLE_USERINFO_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'}
    )
    ensure_google_oauth_token_is_validated(response.status_code)
    user_info = response.json()
    return response_oauth_token_recognized(
        user_info, 
        GOOGLE_OAUTH_PROVIDER
    )


@app.route('/v1/oauth/google/access', methods=['GET', 'POST'])
def oauth_google_validate() -> Response:
    data = flask_incoming_request.headers
    ensure_google_oauth_token_is_present(data)
    token = data.get('X-OAuth-Token')
    response = requests.get(
        GOOGLE_USERINFO_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'}
    )
    ensure_google_oauth_token_is_validated(response.status_code)
    user_info = response.json()
    account = find_or_create_oauth_managed_account(
        current_app.config['MONGODB'], 
        GOOGLE_OAUTH_PROVIDER, 
        user_info
    )
    jwt_secret = current_app.config['JWT_SECRET']
    jwt_token = create_jwt_token(account, jwt_secret, timedelta(days=1))
    return response_access_garanted_success_response(
        account, jwt_token
    )
