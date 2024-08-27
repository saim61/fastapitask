import pytest
from fastapi.testclient import TestClient
from main import app
from starlette import status
from models.users import delete_all_users, insert_user, SignUpUserRequest

client = TestClient(app)

@pytest.fixture
def user_data():
    return SignUpUserRequest(username="test@example.com", password="testpassword", name="Test user")

def test_sign_up():
    delete_all_users()
    response = client.post("/user/sign_up", json={"username": "test@example.com", "password": "testpassword", "name": "Test User"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "Sign up successful"

def test_sign_up_invalid_username():
    response = client.post("/user/sign_up", json={"username": "test", "password": "testpassword", "name": "Test User"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid type of username"

def test_sign_up_duplicate_username(user_data):
    delete_all_users()
    insert_user(user_data)
    response = client.post("/user/sign_up", json={"username": "test@example.com", "password": "testpassword", "name": "Test User"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User already exists"