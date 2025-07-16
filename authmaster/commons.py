from hashlib import sha256
from datetime import *
import jwt as pyjwt


def encrypth_password_sha256(salted_password: str) -> str:
    encoded_password = salted_password.encode()
    return sha256(encoded_password).hexdigest()


def encrypth_password_md5(salted_password: str) -> str:
    encoded_password = salted_password.encode()
    return sha256(encoded_password).hexdigest()


def current_timestamp_datetime() -> datetime:
    return datetime.now(timezone.utc)


def encrypth_password(salted_password: str, algo: str) -> str:
    if algo == "sha256":
        return encrypth_password_sha256(salted_password)
    if algo == "md5":
        return encrypth_password_md5(salted_password)
    raise ValueError(f"Unsupported hashing algorithm: {algo}")


def create_jwt_token(account: dict, secret_key: str, duration: timedelta) -> str:
    payload = {
        'id': str(account['_id']),
        'username': account['uname'],
        'exp': current_timestamp_datetime() + duration
    }
    return pyjwt.encode(payload, secret_key, algorithm='HS256')
