
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime, Text, BIGINT
from sqlalchemy.orm import relationship, Session

from app.models import Users
from app.models.base_model import Base


class Posts(Base):
    __tablename__= "posts"
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(BIGINT, ForeignKey(Users.id), nullable=False)
    user_name = Column(String, nullable=False)
    view_cnt = Column(Integer, nullable=False)
    edit_cnt = Column(Integer, nullable=True)
    del_y = Column(Boolean, default=False)
    
    def __init__(self,title, content, user_id, user_name, view_cnt, edit_cnt, del_y):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.user_name = user_name
        self.view_cnt = view_cnt
        self.edit_cnt = edit_cnt
        self.del_y = del_y
    
    @classmethod
    def get(cls, session: Session, id:int = None, **kwargs):
        if id:
            return session.query(cls).filter_by(id=id, **kwargs).first()
        return session.query(cls).filter_by(**kwargs).first() # 혹은 all 
    
    @classmethod
    def update(cls, session: Session, id: int, **kwargs):
        session.query(cls).filter_by(id=id).update(kwargs)
        session.commit()
