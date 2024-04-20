from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from typing import List
from fastapi.security import HTTPBearer
from starlette.requests import Request

from app import models, schemas
from app.db.connection import db
from app.exception.exceptions import *
from app.controller import post_crud as crud


HTTP_BEARER = HTTPBearer(auto_error=False)
router = APIRouter()

# 게시글 작성
@router.post("/create")
async def create_post(
    request: Request, 
    data: schemas.NewPostReq, 
    session: Session = Depends(db.session),_=Depends(HTTP_BEARER)):
    user = session.query(models.Users).get(request.state.user.id)
    return crud.insert_post(data,user,session)

# 게시글 수정
@router.patch("/update/post")
async def update_post(
    request: Request, 
    data: schemas.UpdateContentReq, 
    session: Session = Depends(db.session),_=Depends(HTTP_BEARER)):
    user = session.query(models.Users).get(request.state.user.id)
    return crud.update_content(data,user, session)

# 게시글 삭제
@router.delete("/delete/post")
async def delete_post(
    request: Request,
    data: schemas.DeletContentReq,
    session: Session = Depends(db.session),_=Depends(HTTP_BEARER)):
    user = session.query(models.Users).get(request.state.user.id)
    return crud.delete_content(data,user,session)    

