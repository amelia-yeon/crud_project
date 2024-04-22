import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user_models import Users
from app.db.connection import db
from app.models import *
from app.utils.auth_utils import hash_password
from main import start_app
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status, Request, Response
from unittest.mock import MagicMock
from app.api.user_api import user
from app.exception.exceptions import *


@pytest.fixture(scope="session")
def mock_db_session():
    """Create a mock database session for use in tests."""
    session = MagicMock(spec=Session)
    session.add = MagicMock()
    session.commit = MagicMock()
    session.delete = MagicMock()
    session.rollback = MagicMock()
    session.query = MagicMock()
    return session

@pytest.fixture(scope="session")
def app(mock_db_session):
    """Create and configure a new app instance for each test, with database dependencies mocked."""
    os.environ['FASTAPI_ENV'] = "test"
    app = start_app()

    app.dependency_overrides[db.session] = lambda: mock_db_session

    @app.exception_handler(BaseException)
    def bad_request_exception_handler(request: Request, exc: BaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"msg": exc.msg}
        )
    
    return app

@pytest.fixture(scope="session")
def client(app):
    with TestClient(app) as client:
        yield client




