from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime


class NewPostReq(BaseModel):
    title: str = Field(max_length=100, description = "The title of the post")
    content: str | None
    
class PostRes(BaseModel):
    title: str
    post_id: int
    success: bool
    
    class Config:
        orm_mode = True

class UpdateContentReq(BaseModel):
    post_id : int
    content: str

class DeletContentReq(BaseModel):
    post_id: int

class GetBoardsRes(BaseModel):
    # 제목, 작성자, 조회수 
    title: str
    name: str
    view_cnt: int

class GetContentsRes(BaseModel):
    name : str
    content: str
    title: str
    created_at: datetime
    updated_at: datetime | str | None 