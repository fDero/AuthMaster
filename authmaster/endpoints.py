from flask import Flask, jsonify
import requests
from flask import request as flask_incoming_request
from __init__ import *

@app.route('/ping', methods=['GET', 'HEAD'])
def ping():
    return jsonify({"message": "ping request recieved correctly"})

@app.route('/oauth/google', methods=['POST'])
def oauth_google():
    data = flask_incoming_request.get_json()
    token = data.get('oauth-token')

    if not token:
        return jsonify({"error": "Missing 'oauth-token' in request body"}), 400

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(GOOGLE_USERINFO_ENDPOINT, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return jsonify({ 
            "status": "success",
            "user": {
                "email": user_info.get("email"),
                "name": user_info.get("name"),
                "id": user_info.get("id"),
                "picture": user_info.get("picture")
            }
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid token",
            "details": response.text
        }), 401