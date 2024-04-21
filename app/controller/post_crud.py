from sqlalchemy.orm import Session
from app import models, schemas
from app.exception.exceptions import *

from loguru import logger

def insert_post(data:schemas.NewPostReq, user, session:Session):
    post = models.Posts(
        title = data.title,
        content = data.content,
        user_id = user.id,
        user_name = user.name,
        view_cnt = 0,
        edit_cnt = 0,
        del_y = True if user.status == "DELETE" else False 
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    
    return schemas.PostRes(
        title = post.title,
        post_id = post.id,
        success= True
    )

def update_content(data:schemas.UpdateContentReq,user,session:Session):
    post_id = models.Posts.get(session,data.post_id)
    try:
        if not post_id:
            raise BadRequestException("존재하지 않는 게시글 번호입니다.")
        
        if post_id.user_id == user.id:
            # post_id.content = f"{post_id.content} {data.content}".strip()
            post_id.content = data.content
            post_id.edit_cnt += 1
            session.commit()
            session.refresh(post_id)
        else:
            raise UnauthorizedException("작성자 본인만 수정 가능합니다.")
    
        return schemas.PostRes(
        title = post_id.title,
        post_id= post_id.id,
        success= True
        )
        
    except Exception as e:
        logger.error(e)
        raise BaseException(status_code=500, detail="수정중 에러가 발생했습니다.")

def delete_content(data: schemas.DeletContentReq,user,session:Session):
    post = models.Posts.get(session,data.post_id)
    try:
        if not post:
            raise BadRequestException("존재하지 않는 게시글 번호입니다.")
        
        if post.user_id == user.id:
            session.delete(post)
            session.commit()
        else:
            raise UnauthorizedException("작성자 본인만 삭제 가능합니다.")
        
        return {"message":"delete success"}
    
    except Exception as e:
        logger.error(f"Deletion error for post ID {data.post_id}: {e}")
        session.rollback()
        raise InternalServerException("삭제 중 에러가 발생했습니다.")
    
def get_posts_username(session:Session):
    query = session.query(
        models.Posts.title,
        models.Users.name,
        models.Posts.view_cnt,
        models.Posts.del_y
    ).join(models.Users, models.Posts.user_id == models.Users.id
    ).order_by(models.Posts.view_cnt.desc(), models.Posts.created_at.desc())
    result = query.all()
    return result

def get_post(posts):
    data = []
    for post in posts:
        pre_data =  schemas.GetBoardsRes(
        title = post.title,
        name = "deleted user" if post.del_y else post.name,
        view_cnt = post.view_cnt
        )
        data.append(pre_data)
    return data

def get_content(post):
    
    data = schemas.GetContentsRes(
        name = post.user_name,
        content = post.content,
        title = post.title,
        created_at = post.created_at,
        updated_at = "" if post.edit_cnt == 0 else post.updated_at
        )
    
    return data