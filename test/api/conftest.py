import os
from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.connection import db
from main import start_app



@pytest.fixture(scope="package")
def client():
    
    os.environ['FASTAPI_ENV'] = "prd"
    app = start_app()
    
    with TestClient(app=app, base_url="http://localhost:8000") as client:
        yield client

@pytest.fixture(scope="function", autouse=True)
def session():
    """
    테스트 단위로 작동하며 디비 초기화
    :return:
    """
    sess = next(db.session())
    yield sess
    sess.rollback()


