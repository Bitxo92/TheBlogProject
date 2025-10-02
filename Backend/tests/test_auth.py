from fastapi.testclient import TestClient
from src.backend.main import app

client= TestClient(app)

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword",
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["first_name"] == "Test"
    assert response.json()["last_name"] == "User"
    assert "id" in response.json()
    assert "created_at" in response.json()
    assert "updated_at" in response.json()
    

def test_register_existingUser():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword",
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}
   
   
def test_login_user():
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword",
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] != ""  # Ensure token is not empty

def test_login_invalidUser():
    response = client.post(
        "/auth/login",
        data={
            "username": "invaliduser",
            "password": "wrongpassword",
        }
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
    