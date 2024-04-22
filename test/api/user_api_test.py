# tests/test_user_api.py

import pytest
import bcrypt
from fastapi import FastAPI, Response, Depends, Request
from app.utils.auth_utils import *
from app.models import Users, UserStatus
from app.schemas import UsersREQ, UsersRES
from app.exception.exceptions import *

@pytest.fixture
def user_login_data():
    return {"email":"user@example.com", "pw":"Str!@#123"}


@pytest.fixture
def mock_user():
    user = Users(email="user@example.com", pw="Str!@#123", name="Test")
    return user

def test_signup_new_user(client, mocker, mock_user,mock_db_session):
    # 요청 데이터 준비
    user_data={
        "email": "user@example.com",
        "pw": "Str!@#123",
        "name": "Test"
    }
    mock_user = mock_user
    mock_user.id = 1 
    
    # 모의: 이메일 중복 검사가 None을 반환
    mocker.patch('app.models.Users.get_by_email_and_status', return_value=None)
    
    # 모의: DB 세션의 add와 commit 메서드
    mock_db_session.add = mocker.MagicMock()
    mock_db_session.commit = mocker.MagicMock()

    try:
        response = client.post("users/sign-up", json=user_data)
        assert response.status_code == 201
        assert response.json()['email'] == 'user@example.com'
        assert response.json()['id'] == 1
        
    except Exception as e:
        print(f"Error during API call: {e}")
        
  
def test_signup_existing_user(client, mock_user,mocker):
    # 이미 존재하는 사용자 객체
    existing_user = mock_user
    mocker.patch('app.models.user_models.Users.get_by_email_and_status', return_value=existing_user)
    user_data = {'email': 'user@example.com', 'pw': 'Str!@#123', 'name': 'Existing'}
    response = client.post("users/sign-up", json=user_data)
    
    assert response.status_code == 400
    assert BadRequestException("이미 존재하는 이메일입니다.")


def test_login_success(client, mocker, mock_user, user_login_data):
    # Users 클래스의 get_by_email_and_status 메서드를 모의하여 항상 mock_user를 반환
    mocker.patch('app.models.user_models.Users.get_by_email_and_status', return_value=mock_user)

    # 비밀번호 검증 함수를 모의하여 항상 True를 반환
    mocker.patch('app.utils.auth_utils.is_valid_password', return_value=True)

    # Users 클래스의 get_token 메서드를 모의하여 토큰 정보를 반환
    mocker.patch('app.models.user_models.Users.get_token', return_value={
        "access_token": "1234",
        "refresh_token": "abcde"
    })
    mocker.patch.object(Response, 'set_cookie')
    
    try:
        response = client.post("users/login", json=user_login_data)
        assert response.status_code == 200
        assert response.json() == {"message": "Login Success"}
        # 응답 헤더에서 토큰 검증
        assert response.headers['Access-Token'] == "1234"
        assert response.headers['Refresh-Token'] == "abcde"
        
    except Exception as e:
        print(f"Error during API call: {e}")


def test_login_invalid_email(client, user_login_data, mocker):
    mocker.patch('app.models.Users.get_by_email_and_status', return_value=None)
    response = client.post("users/login", json=user_login_data)
    
    assert response.status_code == 404
    assert NotFoundException("존재하지 않는 이메일입니다.")

def test_login_invalid_password(client, user_login_data, mocker):
    active_user = Users(email="user@example.com", pw="Str!@#12345", name="Test User")
    mocker.patch('app.api.user_api.Users.get_by_email_and_status', return_value=active_user)
    mocker.patch('app.utils.auth_utils.is_valid_password',return_value=False)  # 비밀번호 불일치
    response = client.post("users/login", json=user_login_data)

    assert response.status_code == 404
    assert NotFoundException("비밀번호가 일치하지 않습니다.")

