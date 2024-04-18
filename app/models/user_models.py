import enum
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, Session
from datetime import datetime, timedelta
from app.models.base_model import Base
from app.utils.utils import *
from app.utils.auth_utils import *

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
    
    @classmethod
    def get(cls, session: Session, id: int = None, **kwargs):
        if id:
            return session.query(cls).filter_by(id=id, **kwargs).first()
        return session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def get_by_email(cls, session: Session, email: str):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def update(cls, session: Session, id: int, **kwargs):
        session.query(cls).filter_by(id=id).update(kwargs)
        session.commit()

