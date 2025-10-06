from fastapi.testclient import TestClient
from src.backend.main import app
###############################################
# Test CRUD operations for User endpoints
###############################################
client = TestClient(app)
test_user_id = None

###############################################
# Test Create User
###############################################

def test_create_user():
    global test_user_id
    response = client.post(
        "/users/createuser/",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            
        },
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"
    assert "id" in response.json()  
    assert "created_at" in response.json()
    assert "updated_at" in response.json()
    test_user_id = response.json()["id"]

def test_create_user_duplicate_email():
    response = client.post(
        "/users/createuser/",
        json={
            "username": "anotheruser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "first_name": "Another",
            "last_name": "User",
        },
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_create_user_duplicate_username():
    response = client.post(
        "/users/createuser/",
        json={
            "username": "testuser",
            "email": "anothertestuser@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        },
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_create_user_missing_fields():
    response = client.post(
        "/users/createuser/",
        json={
            "username": "incompleteuser",
            "password": "testpassword",
        },
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()

###############################################
# Test Get User by ID, Email, ALL Users
###############################################

def test_get_user_by_id():
    response = client.get(
        f"/users/{test_user_id}",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == test_user_id
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["first_name"] == "Test"
    assert response.json()["last_name"] == "User"
    assert "created_at" in response.json()
    assert "updated_at" in response.json()

def test_get_user_by_email():
    response = client.get(
        f"/users/email/testuser@example.com",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == test_user_id
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["first_name"] == "Test"
    assert response.json()["last_name"] == "User"
    assert "created_at" in response.json()
    assert "updated_at" in response.json()

def test_get_user_id_by_username():
    response = client.get(
        f"/users/username/testuser/id",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    assert response.json() == test_user_id

def test_get_user_id_by_email():
    response = client.get(
        f"/users/email/testuser@example.com/id",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    assert response.json() == test_user_id

def test_get_all_users():
    response = client.get(
        "/users/",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(user["id"] == test_user_id for user in response.json())

###############################################
# Test GETTER ERRORS
###############################################

def test_get_user_by_id_not_found():
    response = client.get(
        "/users/00000000-0000-0000-0000-000000000000",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_user_by_email_not_found():
    response = client.get(
        "/users/email/unknown@example.com",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_user_id_by_username_not_found():
    response = client.get(
        "/users/username/unknownuser/id",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

###############################################
# Test Update User
###############################################

def test_update_user():
    response = client.put(
        f"/users/update/{test_user_id}",
        json={
            "username": "newtestuser",
            "first_name": "TestUpdated",
            "last_name": "UserUpdated",
            "email": "testuserupdated@example.com",
            "password": "newpassword"
        },
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == test_user_id
    assert response.json()["username"] == "newtestuser"
    assert response.json()["email"] == "testuserupdated@example.com"
    assert response.json()["first_name"] == "TestUpdated"
    assert response.json()["last_name"] == "UserUpdated"
    assert "created_at" in response.json()
    assert "updated_at" in response.json()

def test_update_user_not_found():
    response = client.put(
        "/users/update/00000000-0000-0000-0000-000000000000",
        json={
            "username": "nonexistentuser",
            "email": "nonexistent@example.com",
            "first_name": "Nonexistent",
            "last_name": "User",
            "password": "nonexistentpassword"
        },
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

###############################################
# Test Delete User
###############################################

def test_delete_user():
    response = client.delete(
        f"/users/{test_user_id}",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 204

def test_get_deleted_user():
    response = client.get(
        f"/users/{test_user_id}",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
 