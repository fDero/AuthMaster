import pymongo
from hashlib import sha256
from random import randint
from exceptions import *
from __init__ import *


def mongodb_connection_setup(args) -> pymongo.collection.Collection:
    mongo_client = pymongo.MongoClient(args.mongodb_connection_string)
    mongo_db = mongo_client[args.mongodb_database_name]
    mongo_collection = mongo_db[args.mongodb_collection_name]
    mongo_collection.create_index("uname", unique=True)
    mongo_collection.create_index("email", unique=True)
    return mongo_collection


def get_hashed_password_object(salt: str, plain_text_password: str) -> dict:
    salted_password = f"{salt}{plain_text_password}"
    encoded_password = salted_password.encode()
    return {
        "hash": sha256(encoded_password).hexdigest(),
        "salt": salt,
        "algo": "sha256"
    }


def get_registration_timestamp_object() -> dict:
    from datetime import datetime
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "timezone": "UTC",
        "format": "ISO 8601"
    }


def get_new_account_status_object() -> dict:
    otp_code = randint(10000, 99999)
    return {
        "status": "unverified",
        "email-otp": str(otp_code), 
        "attempts": 0,
    }


def register_with_authmaster(mongodb, db_owner: str, email: str, username: str, plain_text_password: str) -> dict:
    account = {
        "owner": db_owner,
        "email": email,        
        "state": get_new_account_status_object(),
        "uname": username,
        "passw": get_hashed_password_object(salt=email, plain_text_password=plain_text_password),
        "since": get_registration_timestamp_object()
    }
    try:
        res = mongodb.insert_one(account)
        account["_id"] = str(res.inserted_id)
        return account

    except pymongo.errors.DuplicateKeyError:
        raise AccountAlreadyExistsException()
    
    except Exception:
        raise DatabaseErrorException()


def perform_otp_verification_and_update(mongodb, account: dict, otp: str):
    attempts = account['state']['attempts']
    wrong = account['state']['email-otp'] != otp
    email = account['email']
    failure = attempts >= 2 and wrong
    if failure:
        mongodb.remove({"email": email})
        raise TooManyVerificationAttemptsException()
    elif wrong:
        mongodb.update_one(
            {"email": email},
            {"$set": {"state.attempts": account['state']['attempts'] + 1}}
        )
        raise VerificationAttemptFailedException()
    else:
        mongodb.update_one(
            {"email": email},
            {"$set": {"state.status": "verified"}}
        )


def find_account_in_database(mongodb, data: dict) -> dict:
    email = data.get('email')
    username = data.get('username')
    if email:
        return mongodb.find_one({"email": email})
    else:
        return mongodb.find_one({"uname": username})