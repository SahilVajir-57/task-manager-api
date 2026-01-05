import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_project_success(client: AsyncClient, auth_headers):
    response = await client.post(
        "/projects",
        json={"name": "Test Project", "description": "A test project"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "A test project"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_project_no_description(client: AsyncClient, auth_headers):
    response = await client.post(
        "/projects",
        json={"name": "Minimal Project"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Minimal Project"
    assert data["description"] is None


@pytest.mark.asyncio
async def test_create_project_unauthorized(client: AsyncClient):
    response = await client.post(
        "/projects",
        json={"name": "Test Project"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_project_empty_name(client: AsyncClient, auth_headers):
    response = await client.post(
        "/projects",
        json={"name": ""},
        headers=auth_headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_projects(client: AsyncClient, auth_headers):
    # Create two projects
    await client.post("/projects", json={"name": "Project 1"}, headers=auth_headers)
    await client.post("/projects", json={"name": "Project 2"}, headers=auth_headers)
    
    response = await client.get("/projects", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert len(data["projects"]) >= 2


@pytest.mark.asyncio
async def test_get_project_success(client: AsyncClient, auth_headers):
    # Create a project
    create_response = await client.post(
        "/projects",
        json={"name": "Get Test Project"},
        headers=auth_headers,
    )
    project_id = create_response.json()["id"]
    
    # Get the project
    response = await client.get(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Get Test Project"
    assert data["id"] == project_id


@pytest.mark.asyncio
async def test_get_project_not_found(client: AsyncClient, auth_headers):
    response = await client.get("/projects/nonexistent-id", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


@pytest.mark.asyncio
async def test_update_project_success(client: AsyncClient, auth_headers):
    # Create a project
    create_response = await client.post(
        "/projects",
        json={"name": "Original Name"},
        headers=auth_headers,
    )
    project_id = create_response.json()["id"]
    
    # Update the project
    response = await client.put(
        f"/projects/{project_id}",
        json={"name": "Updated Name", "description": "New description"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "New description"


@pytest.mark.asyncio
async def test_update_project_partial(client: AsyncClient, auth_headers):
    # Create a project
    create_response = await client.post(
        "/projects",
        json={"name": "Original", "description": "Original desc"},
        headers=auth_headers,
    )
    project_id = create_response.json()["id"]
    
    # Update only the name
    response = await client.put(
        f"/projects/{project_id}",
        json={"name": "New Name"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"


@pytest.mark.asyncio
async def test_update_project_not_found(client: AsyncClient, auth_headers):
    response = await client.put(
        "/projects/nonexistent-id",
        json={"name": "Test"},
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_project_success(client: AsyncClient, auth_headers):
    # Create a project
    create_response = await client.post(
        "/projects",
        json={"name": "To Delete"},
        headers=auth_headers,
    )
    project_id = create_response.json()["id"]
    
    # Delete the project
    response = await client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = await client.get(f"/projects/{project_id}", headers=auth_headers)
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_project_not_found(client: AsyncClient, auth_headers):
    response = await client.delete("/projects/nonexistent-id", headers=auth_headers)
    assert response.status_code == 404