

import string
import bcrypt
from datetime import timedelta, datetime
import jwt
import string
from datetime import datetime
from config import get_env

from app.utils.utils import *
from app.exception.exceptions import *

def create_token(data: dict, delta: int):
    conf = get_env()
    expire = get_current_utc_time() + timedelta(minutes=delta)
    payload = dict(exp=expire, **data)
    payload["iat"] = get_current_utc_time()
    payload["iss"] = "test api"
    encoded_jwt = jwt.encode(payload, conf.JWT_SECRET_KEY, algorithm=conf.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    conf = get_env()
    try:
        payload = jwt.decode(token, conf.JWT_SECRET_KEY, algorithms=conf.JWT_ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("토큰이 만료되었습니다.")
    except jwt.InvalidTokenError:
        raise Exception("토큰이 유효하지 않습니다.")

def hash_password(password: str):
    if len(password) < 8:
        raise BadRequestException("패스워드의 길이는 8자 보다 길어야 합니다.")
    if not any(char in string.punctuation for char in password):
        raise BadRequestException("패스워드에 최소한 1개 이상의 특수문자가 포함되어야 합니다.")
    if not any(char.isupper() for char in password):
        raise BadRequestException("패스워드에 최소한 1개 이상의 대문자가 포함되어야 합니다.")
    if not any(char.islower() for char in password):
        raise BadRequestException("패스워드에 최소한 1개 이상의 소문자가 포함되어야 합니다.")
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def is_valid_password(password: str, hashed_password: str):
    try:
        is_verified = bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
        return is_verified
    except Exception:
        return False