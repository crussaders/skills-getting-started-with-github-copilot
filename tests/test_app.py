import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No special setup required)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_prevent_duplicate():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Act
    response_first = client.post(f"/activities/{activity}/signup", params={"email": email})
    response_duplicate = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response_first.status_code == 200
    assert response_duplicate.status_code == 400
    assert "already signed up" in response_duplicate.json()["detail"]

def test_unregister_participant():
    # Arrange
    email = "removeuser@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response_remove = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    response_remove_again = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response_remove.status_code == 200
    assert response_remove_again.status_code == 404

def test_signup_activity_not_found():
    # Arrange
    email = "nobody@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404

def test_unregister_activity_not_found():
    # Arrange
    email = "nobody@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
