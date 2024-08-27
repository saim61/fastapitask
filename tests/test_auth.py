import pytest
from fastapi.testclient import TestClient
from main import app
from starlette import status
from models.users import delete_all_users, insert_user, SignUpUserRequest


client = TestClient(app)
def test_login_success():
    delete_all_users()
    client.post("/user/sign_up", json={"username": "test@example.com", "password": "testpassword", "name": "Test User"})

    # Arrange
    username = "test@example.com"
    password = "testpassword"
    form_data = {"username": username, "password": password}

    # Act
    response = client.post("/auth/token", data=form_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["message"] == "Token is valid for 5 minutes!"

def test_login_invalid_credentials():
    delete_all_users()
    client.post("/user/sign_up", json={"username": "test@example.com", "password": "testpassword", "name": "Test User"})

    # Arrange
    username = "invalid_username"
    password = "testpassword"
    form_data = {"username": username, "password": password}

    # Act
    response = client.post("/auth/token", data=form_data)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials. Please try again or sign up."