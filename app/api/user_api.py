from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.connection import db
from app.exception.exceptions import *
from app.utils.auth_utils import *
from app.models import *

user = APIRouter()

# 회원가입 API
@user.post("/sign-up", response_model=schemas.UsersRES, status_code=201)
async def register(data: schemas.UsersREQ, session: Session = Depends(db.session)):
    u = models.Users(email=data.email, pw=data.pw, name=data.name)
    if models.Users.get_by_email_and_status(session,data.email, models.UserStatus.ACTIVE):
        raise BadRequestException("이미 존재하는 이메일입니다.")
    session.add(u)
    session.commit()
    return u

# login API
@user.post("/login")
async def login(data: schemas.UserLogin,session: Session = Depends(db.session),response:Response = None):
    u = models.Users.get_by_email(session, data.email)
    if not u:
        raise BadRequestException("존재하지 않는 이메일입니다.")
    if not is_valid_password(data.pw, u.pw):
        raise BadRequestException("비밀번호가 일치하지 않습니다")

    
    return {"message": "Login Success"}


