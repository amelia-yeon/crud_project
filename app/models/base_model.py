from app.utils.utils import *

from sqlalchemy import Column, BIGINT, DateTime
from sqlalchemy.orm import as_declarative
from sqlalchemy.sql import func

@as_declarative()
class Base:
    __table_args__={"schema":"viva"}
    id = Column(BIGINT, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)



