from hashlib import *
from datetime import *
from secrets import *
import jwt as pyjwt


def get_random_string(length: int = 16) -> str:
    return token_urlsafe(length)


def encrypth_password_sha256(salted_password: str) -> str:
    encoded_password = salted_password.encode()
    return sha256(encoded_password).hexdigest()


def encrypth_password_md5(salted_password: str) -> str:
    encoded_password = salted_password.encode()
    return md5(encoded_password).hexdigest()


def current_timestamp_datetime() -> datetime:
    return datetime.now(timezone.utc)


def encrypth_password(salted_password: str, algo: str) -> str:
    encrypth_callbacks = {
        'sha256': encrypth_password_sha256,
        'md5': encrypth_password_md5
    }
    return encrypth_callbacks[algo](salted_password)


def create_jwt_token(account: dict, secret_key: str, duration: timedelta) -> str:
    payload = {
        'id': str(account['_id']),
        'username': account['uname'],
        'exp': current_timestamp_datetime() + duration
    }
    return pyjwt.encode(payload, secret_key, algorithm='HS256')
