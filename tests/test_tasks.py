import pytest
from httpx import AsyncClient


@pytest.fixture
async def test_project(client: AsyncClient, auth_headers):
    response = await client.post(
        "/projects",
        json={"name": "Task Test Project"},
        headers=auth_headers,
    )
    return response.json()


@pytest.mark.asyncio
async def test_create_task_success(client: AsyncClient, auth_headers, test_project):
    response = await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Test Task", "description": "A test task"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "A test task"
    assert data["status"] == "todo"
    assert data["priority"] == "medium"
    assert data["project_id"] == test_project["id"]


@pytest.mark.asyncio
async def test_create_task_with_priority(client: AsyncClient, auth_headers, test_project):
    response = await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "High Priority Task", "priority": "high"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["priority"] == "high"


@pytest.mark.asyncio
async def test_create_task_invalid_project(client: AsyncClient, auth_headers):
    response = await client.post(
        "/projects/nonexistent-id/tasks",
        json={"title": "Test Task"},
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


@pytest.mark.asyncio
async def test_create_task_unauthorized(client: AsyncClient, test_project):
    response = await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Test Task"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_task_empty_title(client: AsyncClient, auth_headers, test_project):
    response = await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": ""},
        headers=auth_headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient, auth_headers, test_project):
    # Create tasks
    await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Task 1"},
        headers=auth_headers,
    )
    await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Task 2"},
        headers=auth_headers,
    )
    
    response = await client.get(
        f"/projects/{test_project['id']}/tasks",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert len(data["tasks"]) >= 2
    assert "page" in data
    assert "per_page" in data
    assert "total_pages" in data


@pytest.mark.asyncio
async def test_list_tasks_filter_by_status(client: AsyncClient, auth_headers, test_project):
    # Create tasks with different statuses
    await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Todo Task", "status": "todo"},
        headers=auth_headers,
    )
    await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Done Task", "status": "done"},
        headers=auth_headers,
    )
    
    # Filter by status
    response = await client.get(
        f"/projects/{test_project['id']}/tasks?status=todo",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    for task in data["tasks"]:
        assert task["status"] == "todo"


@pytest.mark.asyncio
async def test_list_tasks_filter_by_priority(client: AsyncClient, auth_headers, test_project):
    # Create tasks with different priorities
    await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "High Task", "priority": "high"},
        headers=auth_headers,
    )
    await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Low Task", "priority": "low"},
        headers=auth_headers,
    )
    
    # Filter by priority
    response = await client.get(
        f"/projects/{test_project['id']}/tasks?priority=high",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    for task in data["tasks"]:
        assert task["priority"] == "high"


@pytest.mark.asyncio
async def test_get_task_success(client: AsyncClient, auth_headers, test_project):
    # Create a task
    create_response = await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Get Test Task"},
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]
    
    # Get the task
    response = await client.get(
        f"/projects/{test_project['id']}/tasks/{task_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get Test Task"
    assert data["id"] == task_id


@pytest.mark.asyncio
async def test_get_task_not_found(client: AsyncClient, auth_headers, test_project):
    response = await client.get(
        f"/projects/{test_project['id']}/tasks/nonexistent-id",
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


@pytest.mark.asyncio
async def test_update_task_success(client: AsyncClient, auth_headers, test_project):
    # Create a task
    create_response = await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Original Title"},
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]
    
    # Update the task
    response = await client.put(
        f"/projects/{test_project['id']}/tasks/{task_id}",
        json={"title": "Updated Title", "status": "in_progress"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "in_progress"


@pytest.mark.asyncio
async def test_update_task_partial(client: AsyncClient, auth_headers, test_project):
    # Create a task
    create_response = await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "Original", "priority": "low"},
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]
    
    # Update only status
    response = await client.put(
        f"/projects/{test_project['id']}/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    assert data["title"] == "Original"
    assert data["priority"] == "low"


@pytest.mark.asyncio
async def test_update_task_not_found(client: AsyncClient, auth_headers, test_project):
    response = await client.put(
        f"/projects/{test_project['id']}/tasks/nonexistent-id",
        json={"title": "Test"},
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_success(client: AsyncClient, auth_headers, test_project):
    # Create a task
    create_response = await client.post(
        f"/projects/{test_project['id']}/tasks",
        json={"title": "To Delete"},
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = await client.delete(
        f"/projects/{test_project['id']}/tasks/{task_id}",
        headers=auth_headers,
    )
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = await client.get(
        f"/projects/{test_project['id']}/tasks/{task_id}",
        headers=auth_headers,
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_found(client: AsyncClient, auth_headers, test_project):
    response = await client.delete(
        f"/projects/{test_project['id']}/tasks/nonexistent-id",
        headers=auth_headers,
    )
    assert response.status_code == 404