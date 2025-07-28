import pymongo
from commons import *
from random import randint
from commons import *
from exceptions import *
from __init__ import *


def mongodb_connection_setup(args) -> pymongo.collection.Collection:
    mongo_client = pymongo.MongoClient(args.mongodb_connection_string)
    mongo_db = mongo_client[args.mongodb_database_name]
    mongo_collection = mongo_db[args.mongodb_collection_name]
    mongo_collection.create_index('uname', unique=True)
    mongo_collection.create_index('email', unique=True)
    return mongo_collection


def get_hashed_password_object(salt: str, plain_text_password: str, algo: str) -> dict:
    salted_password = f'{salt}{plain_text_password}'
    return {
        'hash': encrypth_password(salted_password, algo),
        'salt': salt,
        'algo': algo
    }


def get_registration_timestamp_object() -> dict:
    return {
        'timestamp': current_timestamp_datetime(),
        'timezone': 'UTC',
        'format': 'ISO 8601'
    }


def get_new_account_status_object() -> dict:
    otp_code = randint(10000, 99999)
    return {
        'status': 'unverified',
        'email-otp': str(otp_code), 
        'attempts': 0,
    }


def get_new_oauth_account_status_object(oauth_provider : str, oauth_id : str) -> dict:
    otp_code = randint(10000, 99999)
    return {
        'status': 'verified',
        'oauth-provider': oauth_provider,
        'oauth-id': oauth_id,
    }


def register_with_authmaster(mongodb, db_owner: str, algo: str, email: str, username: str, plain_text_password: str) -> dict:
    salt = get_random_string(32)
    account = {
        'owner': db_owner,
        'email': email,        
        'state': get_new_account_status_object(),
        'uname': username,
        'passw': get_hashed_password_object(salt, plain_text_password, algo),
        'since': get_registration_timestamp_object()
    }
    try:
        res = mongodb.insert_one(account)
        account['_id'] = str(res.inserted_id)
        return account

    except pymongo.errors.DuplicateKeyError:
        raise AccountAlreadyExistsException()
    
    except Exception:
        raise DatabaseErrorException()


def perform_otp_verification_and_update(mongodb, account: dict, otp: str):
    attempts = account['state']['attempts']
    wrong = account['state']['email-otp'] != otp
    email = account['email']
    if attempts >= 2 and wrong:
        mongodb.remove({'email': email})
        raise TooManyVerificationAttemptsException()
    new_status = 'unverified' if wrong else 'verified'
    new_attempts = attempts + (1 if wrong else 0)
    mongodb.update_one(
        {'email': email},
        {'$set': {'state.attempts': new_attempts, 'state.status': new_status}}
    )


def find_account_in_database(mongodb, data: dict) -> dict:
    email = data.get('email')
    username = data.get('username')
    if email:
        return mongodb.find_one({'email': email})
    else:
        return mongodb.find_one({'uname': username})


def find_account_by_oauth_id(mongodb, provider: str, oauth_id: str) -> dict:
    return mongodb.find_one({
        'state.oauth-provider': provider,
        'state.oauth-id': oauth_id
    })


def create_oauth_managed_account(mongodb, provider: str, data: dict) -> dict:
    oauth_id = data.get('id')
    new_account = mongodb.insert_one({
        'owner': 'third-party',
        'email': data.get('email'),
        'uname': data.get('name'),
        'state': get_new_oauth_account_status_object(provider, oauth_id),
        'since': get_registration_timestamp_object()
    })
    new_account['_id'] = str(new_account.inserted_id)
    return new_account


def find_or_create_oauth_managed_account(mongodb, provider: str, data: dict) -> dict:
    search_result = find_account_by_oauth_id(mongodb, provider, data.get('id'))
    if not search_result:
        return create_oauth_managed_account(mongodb, provider, data)
    return search_result 