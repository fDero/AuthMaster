from __init__ import *
from flask import jsonify
from flask import request as flask_incoming_request
from http import HTTPStatus
from exceptions import *
import requests

@app.route('/ping', methods=['GET', 'HEAD'])
def ping():
    return jsonify({"message": "ping request recieved correctly"})


@app.route('/oauth/google', methods=['POST'])
def oauth_google():
    data = flask_incoming_request.get_json()
    token = data.get('oauth-token')
    if not token: 
        raise MissingOAuthTokenException()

    response = requests.get(GOOGLE_USERINFO_ENDPOINT)
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
