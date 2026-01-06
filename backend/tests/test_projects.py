import pytest
from fastapi import status


def get_auth_token(client):
    """Helper to get auth token."""
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    return response.json()["access_token"]


def test_create_project(client):
    """Test creating a project."""
    token = get_auth_token(client)
    response = client.post(
        "/api/v1/projects",
        json={"name": "Test Project", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "Test Description"
    assert "id" in data


def test_get_projects(client):
    """Test getting all projects."""
    token = get_auth_token(client)
    client.post(
        "/api/v1/projects",
        json={"name": "Project 1"},
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/v1/projects",
        json={"name": "Project 2"},
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_get_project_by_id(client):
    """Test getting a project by ID."""
    token = get_auth_token(client)
    create_response = client.post(
        "/api/v1/projects",
        json={"name": "Test Project"},
        headers={"Authorization": f"Bearer {token}"},
    )
    project_id = create_response.json()["id"]
    response = client.get(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == project_id


def test_update_project(client):
    """Test updating a project."""
    token = get_auth_token(client)
    create_response = client.post(
        "/api/v1/projects",
        json={"name": "Old Name"},
        headers={"Authorization": f"Bearer {token}"},
    )
    project_id = create_response.json()["id"]
    response = client.put(
        f"/api/v1/projects/{project_id}",
        json={"name": "New Name"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "New Name"


def test_delete_project(client):
    """Test deleting a project."""
    token = get_auth_token(client)
    create_response = client.post(
        "/api/v1/projects",
        json={"name": "Test Project"},
        headers={"Authorization": f"Bearer {token}"},
    )
    project_id = create_response.json()["id"]
    response = client.delete(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    get_response = client.get(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

