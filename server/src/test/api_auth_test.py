from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)


def test_login():
    response = client.post(
        "api/auth/login",
        headers={"Content-Type": "application/json"},
        json={"email": "tolga123@gmail.com", "password": "tolga123"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Login is successful."}


def test_register():
    response = client.post(
        "api/auth/register",
        headers={"Content-Type": "application/json"},
        json={
            "username": "azra1231",
            "email": "azra1231@gmail.com",
            "password": "azra1231",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Account created."}


def test_logout():
    response = client.post("api/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "You are logged out."}

