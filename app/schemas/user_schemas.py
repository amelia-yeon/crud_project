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