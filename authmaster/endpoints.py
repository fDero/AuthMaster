from flask import Flask, jsonify
import requests
from flask import request as flask_incoming_request
from __init__ import *

@app.route('/ping', methods=['GET', 'HEAD'])
def ping():
    return jsonify({"message": "ping request recieved correctly"})