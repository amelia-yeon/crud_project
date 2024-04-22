from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.connection import db
from app.exception.exceptions import *
from app.utils.auth_utils import *
from app.models import *
from app.controller import user_crud as crud_ctrl
from starlette.requests import Request


HTTP_BEARER = HTTPBearer(auto_error=False)
user = APIRouter()

# 회원가입 API
@user.post("/sign-up", response_model=schemas.UsersRES, status_code=201)
async def signup(data: schemas.UsersREQ, session: Session = Depends(db.session)):
    u = models.Users(email=data.email, pw=data.pw, name=data.name)
    if models.Users.get_by_email_and_status(session,data.email, models.UserStatus.ACTIVE):
        raise BadRequestException("이미 존재하는 이메일입니다.")
    session.add(u)
    session.commit()
    return u

# login API
@user.post("/login")
async def login(data: schemas.UserLogin,session: Session = Depends(db.session),response:Response = None):
    u = models.Users.get_by_email_and_status(session,data.email, models.UserStatus.ACTIVE)
    if not u:
        raise NotFoundException("존재하지 않는 이메일입니다.")
    if not is_valid_password(data.pw, u.pw):
        raise NotFoundException("비밀번호가 일치하지 않습니다.")
    return crud_ctrl.login_user(u,session,response)

# Refresh Token 발행 API
@user.post("/refresh-token")
async def refresh_token(data: schemas.RefreshToken, session: Session = Depends(db.session),response:Response = None):
    refresh_payload = decode_token(data.refresh_token)
    u = session.query(models.Users).filter_by(id=refresh_payload["id"]).first()
    token = u.token_refresh(session, data.refresh_token)
    
    return crud_ctrl.token_issued(token,response)

# 유저 정보 수정 update API
@user.post("/update/info")
async def update_user(
    request: Request, 
    data: schemas.UpdateUser, 
    session: Session = Depends(db.session),_=Depends(HTTP_BEARER),
    response:Response = None):
    user = session.query(models.Users).get(request.state.user.id)
    
    return crud_ctrl.update_info(data,user,session,response)

# 회원 탈퇴 API
@user.post("/status/delete")
async def delete_user(
    request: Request, 
    session: Session = Depends(db.session),_=Depends(HTTP_BEARER)):
    user = session.query(models.Users).get(request.state.user.id)
    
    return crud_ctrl.status_delete(user, session)


