from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.connection import db
from app.exception.exceptions import *
from app.utils.auth_utils import *
from app.models import *

user = APIRouter()

@user.post("/sign-up", response_model=schemas.UsersRES, status_code=201)
async def register(data: schemas.UsersREQ, session: Session = Depends(db.session)):
    u = models.Users(email=data.email, pw=data.pw, name=data.name)
    if models.Users.get_by_email(session, data.email):
        raise BadRequestException("이미 존재하는 이메일입니다.")
    session.add(u)
    session.commit()
    return u

