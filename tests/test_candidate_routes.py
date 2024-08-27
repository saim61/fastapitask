import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from main import app
from starlette import status
from models.candidates import insert_candidate, CandidateRequest
from models.users import delete_all_users

client = TestClient(app)

@pytest.fixture
def token():
    delete_all_users()
    client.post("/user/sign_up", json={"username": "test@example.com", "password": "testpassword", "name": "Test User"})
    form_data = {"username": "test@example.com", "password": "testpassword"}
    response = client.post("/auth/token", data=form_data)
    return response.json()["access_token"]

payload = {
        "gender": "male",
        "name": "Test Candidate",
        "phone": "456-456"
}

def test_add_candidate_without_jwt():
    response = client.post("/candidate/", json={"gender": "male", "name": "Test Candidate", "phone": "456-456"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_add_candidate(token):
    jwt_header = {"Authorization": f"Bearer {token}"}
    response = client.post("/candidate/", headers=jwt_header, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "The candidate was added"

def test_update_candidate(token):
    jwt_header = {"Authorization": f"Bearer {token}"}
    candidate = CandidateRequest(gender=payload["gender"], name=payload["name"], phone=payload["phone"])

    result = insert_candidate(candidate)
    response = client.put(f"/candidate/{result.inserted_id}", headers=jwt_header, json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert  response.json()["detail"] == "The candidate was updated"

def test_update_invalid_candidate(token):
    # invalid id
    _id = ObjectId('66cca8e538b774d25d522abc')

    jwt_header = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/candidate/{_id}", headers=jwt_header, json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Error while updating candidate"

def test_delete_candidate(token):
    candidate = CandidateRequest(gender=payload["gender"], name=payload["name"], phone=payload["phone"])

    result = insert_candidate(candidate)

    jwt_header = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/candidate/{result.inserted_id}", headers=jwt_header)

    assert response.status_code == status.HTTP_200_OK
    assert  response.json()["detail"] == "The candidate was deleted"

def test_delete_invalid_candidate(token):
    # invalid id
    _id = ObjectId('66cca8e538b774d25d522abc')

    jwt_header = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/candidate/{_id}", headers=jwt_header)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Error while deleting candidate"
