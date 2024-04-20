from fastapi import Response
from sqlalchemy.orm import Session
from app import models, schemas
from app.exception.exceptions import *
from app.utils.auth_utils import is_valid_password, decode_token, hash_password
from loguru import logger



def login_user(u,session: Session,response:Response = None):
    token = u.get_token(session)
    response.headers['Access-Token'] = token['access_token']
    response.headers['Refresh-Token'] = token['refresh_token']
    
    return {"message": "Login Success"}


def token_issued(token,response:Response = None):
    if len(token) == 1:
        response.headers['Access-Token'] = token['access_token']
        message = "new access-token 발행"
    else:
        response.headers['Access-Token'] = token['access_token']
        response.headers['Refresh-Token'] = token['refresh_token']
        message = "access & refresh 모두 발급 완료"
    
    return {"message": message}


def update_info(data:schemas.UpdateUser,user,session:Session, response:Response = None):
    update_data = {}
    if data.new_pw:
        update_data['pw'] = hash_password(data.new_pw)
    if data.new_name:
        update_data['name'] = data.new_name
    if update_data:
        models.Users.update(session, user.id, **update_data)
        token = user.get_token(session)
        response.headers['Access-Token'] = token['access_token']
        response.headers['Refresh-Token'] = token['refresh_token']
        return {"value" : "Change Success"}
    else:
        return {"message": "No changes made"}