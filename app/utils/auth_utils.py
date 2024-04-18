
from app.exception.exceptions import *
import string
import bcrypt



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