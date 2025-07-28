from flask import Flask
from hashlib import sha256, md5

app = Flask(__name__)

GOOGLE_OAUTH_PROVIDER = 'Google'
GOOGLE_USERINFO_ENDPOINT  = 'https://www.googleapis.com/oauth2/v3/userinfo'
AVAILABLE_ENCRYPTION_ALGORITHMS = ['sha256', 'md5']