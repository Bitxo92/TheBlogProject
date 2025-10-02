from fastapi.testclient import TestClient
from src.backend.main import app


# Initialize the TestClient with the FastAPI app
client= TestClient(app)


###############################################
# Authentication Tests
###############################################

def test_register_user():
    """
    Test user registration endpoint
    1. Send a POST request to /auth/register with user details
    2. Assert that the response status code is 201 (Created)
    3. Assert that the response JSON contains the correct user details
    4. Assert that the response JSON contains an id, created_at, and updated_at field
    """
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
    """
    Test registration with an existing username
    1. Send a POST request to /auth/register with user details that already exist
    2. Assert that the response status code is 400 (Bad Request)
    3. Assert that the response JSON contains the appropriate error message
    """
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
    """
    Test user login endpoint
    1. Send a POST request to /auth/login with valid credentials
    2. Assert that the response status code is 200 (OK)
    3. Assert that the response JSON contains an access token and token type
    4. Assert that the access token is not empty
    """
    
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
    """
    Test login with invalid credentials
    1. Send a POST request to /auth/login with invalid credentials
    2. Assert that the response status code is 401 (Unauthorized)
    3. Assert that the response JSON contains the appropriate error message
    """
    response = client.post(
        "/auth/login",
        data={
            "username": "invaliduser",
            "password": "wrongpassword",
        }
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
    