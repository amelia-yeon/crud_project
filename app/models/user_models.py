import enum
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, Session
from datetime import datetime, timedelta
from app.utils.utils import *
from app.models.base_model import Base
from app.utils.auth_utils import (
    hash_password,
    create_token,
    decode_token,
)
from config import get_env



class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class Users(Base):
    __tablename__ = "users"
    email = Column(String(64), nullable=False)
    pw = Column(String(256), nullable=False)
    name = Column(String(64), nullable=False, default=False)
    status = Column(Enum(UserStatus, native_enum=False, length=50), nullable=False, default=UserStatus.ACTIVE)
    refresh_token = Column(String(512), nullable=True)
    refresh_token_expiration = Column(DateTime, nullable=True)
    
    
    def __init__(self, email, pw, name):
        self.email = email
        self.pw = hash_password(pw)
        self.name = name
    
    def set_refresh_token(self, token, expires_in):
        self.refresh_token = token
        self.refresh_token_expiration = datetime.utcnow() + timedelta(minutes=expires_in)
        return token
    
    @classmethod
    def get(cls, session: Session, id: int = None, **kwargs):
        if id:
            return session.query(cls).filter_by(id=id, **kwargs).first()
        return session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def get_by_email(cls, session: Session, email: str):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def get_by_email_and_status(cls, session: Session, email: str, status: UserStatus):
        return session.query(cls).filter_by(email=email, status=status).first()
    
    @classmethod
    def update(cls, session: Session, id: int, **kwargs):
        session.query(cls).filter_by(id=id).update(kwargs)
        session.commit()

    def get_token(self,session: Session):
        
        access_token = create_token(
            data=dict(id=self.id, email=self.email),
            delta=get_env().ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token = create_token(
            data=dict(id=self.id),
            delta=get_env().REFRESH_TOKEN_EXPIRE_MINUTES
        )
        
        self.set_refresh_token(refresh_token, get_env().REFRESH_TOKEN_EXPIRE_MINUTES)
        session.add(self)
        session.commit()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }   

    def token_refresh(self, session: Session,refresh_token: str):
        refresh_payload = decode_token(refresh_token)
        now = int(get_current_utc_time().timestamp())
        if now - refresh_payload["iat"] < get_env().REFRESH_TOKEN_EXPIRE_MINUTES * 60 / 2:
            return {
                "access_token": create_token(
                    data=dict(id=self.id, email=self.email),
                    delta=get_env().ACCESS_TOKEN_EXPIRE_MINUTES,
                )
            }
        else:
            return self.get_token(session)

