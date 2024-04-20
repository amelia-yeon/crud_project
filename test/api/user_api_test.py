import pytest

@pytest.mark.parametrize(
    "request_data",
    [
        dict(email="abc@abc.com",pw="string123",name="amelia"),
        dict(email="abc@abc.com",pw="String123",name="amelia"),
        dict(email="abc@2abc.com",pw="string123!@#",name="amelia"),
        dict(email="abc123@abc.com",pw="String123!@#",name="amelia"),
        dict(email="abcd@abccom",pw="String123!@#",name="amelia"),
        dict(email="suyeonabc.com",pw="String123!@#$",name="amelia"),
        dict(email="suyeo@nabc.com",pw="St123!@",name="amelia")
    ]
)


def test_signup(client,session,request_data):
    response = client.post("/user/signup",json=request_data)
    assert response.status_code == 400
    session.rollback()