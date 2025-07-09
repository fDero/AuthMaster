import hashlib
import pymongo
from pymongo import *
from exceptions import *
from __init__ import *

mongo_client = MongoClient(MONGODB_CONNECTION_STRING)
mongo_db = mongo_client[MONGODB_DATABASE_NAME]
mongo_collection = mongo_db[MONGODB_COLLECTION_NAME]

def get_hashed_password_object(salt : str, plain_text_password: str):
    salted_password = f"{salt}{plain_text_password}"
    encoded_password = salted_password.encode()
    return {
        "hash": hashlib.sha256(encoded_password).hexdigest(),
        "salt": salt,
        "algo": "sha256"
    }

def get_registration_timestamp_object():
    from datetime import datetime
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "timezone": "UTC",
        "format": "ISO 8601"
    }

def get_new_account_status_object(email_otp: str):
    return {
        "status": "unverified",
        "email-otp": email_otp, 
        "attempts": 0,
    }

def register_with_authmaster(email: str, username: str, plain_text_password: str):
    mongo_collection.create_index("email", unique=True)
    mongo_collection.create_index("username", unique=True)
    account = {
        "owner": AUTHMASTER_OWNER,
        "email": email,        
        "state": get_new_account_status_object(email_otp=email),
        "uname": username,
        "passw": get_hashed_password_object(email, plain_text_password),
        "since": get_registration_timestamp_object()
    }
    try:
        mongo_collection.insert_one(account)

    except pymongo.errors.DuplicateKeyError:
        raise AccountAlreadyExistsException()
    
    except Exception:
        raise DatabaseErrorException()
