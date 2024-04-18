from app.utils.utils import *

from sqlalchemy import Column, BIGINT, datetime
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    __table_args__={"schema":"viva"}
    id = Column(BIGINT, primary_key=True, index=True)
    created_at = Column(datetime, nullable=True, default=get_current_utc_time)
    updated_at = Column(datetime, nullable=True, default=get_current_utc_time)


