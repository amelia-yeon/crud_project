from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate, add_pagination, LimitOffsetPage
from sqlalchemy.orm import Session
from starlette.requests import Request
from typing import List
from fastapi.security import HTTPBearer
from starlette.requests import Request

from app import models, schemas
from app.db.connection import db
from app.exception.exceptions import *
from app.controller import post_crud as post_ctrl


HTTP_BEARER = HTTPBearer(auto_error=False)
router = APIRouter()

# 게시글 작성
@router.post("/create")
async def create_post(
    request: Request, 
    data: schemas.NewPostReq, 
    session: Session = Depends(db.session),_=Depends(HTTP_BEARER)):
    user = session.query(models.Users).get(request.state.user.id)
    return post_ctrl.insert_post(data,user,session)

# 게시글 수정
@router.patch("/update/post")
async def update_post(
    request: Request, 
    data: schemas.UpdateContentReq, 
    session: Session = Depends(db.session),_=Depends(HTTP_BEARER)):
    user = session.query(models.Users).get(request.state.user.id)
    return post_ctrl.update_content(data,user, session)

# 게시글 삭제
@router.delete("/delete/post")
async def delete_post(
    request: Request,
    data: schemas.DeletContentReq,
    session: Session = Depends(db.session),_=Depends(HTTP_BEARER)):
    user = session.query(models.Users).get(request.state.user.id)
    return post_ctrl.delete_content(data,user,session)    

# 게시글 목록 조회
@router.get("/get/post", response_model=Page[schemas.GetBoardsRes]) 
async def get_post_all(session: Session = Depends(db.session)):
    posts = post_ctrl.get_posts_username(session)
    data = post_ctrl.get_post(posts)
    return paginate(data)

# 게시물 조회 
@router.get("/posts/{post_id}")
def read_post(post_id: int, session: Session = Depends(db.session)):
    post = session.query(models.Posts).filter(models.Posts.id == post_id).first()
    if post is None:
        raise BadRequestException("게시물이 없습니다.")
    post.view_cnt += 1  # 조회수 증가
    session.commit()  # 변경 사항 저장
    return post_ctrl.get_content(post)
