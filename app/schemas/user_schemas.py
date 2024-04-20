from pydantic import BaseModel, EmailStr
from typing import List


class UsersRES(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

class UsersREQ(BaseModel):
    email: EmailStr
    pw: str
    name : str


class UserLogin(BaseModel):
    email : EmailStr
    pw : str
    
class Token(BaseModel):
    access_token: str
    refresh_token: str = None
    
class RefreshToken(BaseModel):
    refresh_token: str

class UpdateUser(BaseModel):
    curr_pw: str
    new_pw : str | None
    new_name : str | None 