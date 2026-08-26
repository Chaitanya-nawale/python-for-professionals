from fastapi.testclient import TestClient

from release_tracker.main import app

client = TestClient(app)


def test_list_projects_with_name():
    response = client.get("/projects/name")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


def test_list_projects_with_slug():
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


def test_list_projects_by_slug():
    response = client.get("/projects", params={"project_slug": "project-a"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["slug"] == "project-a"


def test_get_project():
    response = client.get("/project/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Project A"


def test_get_project_not_found():
    response = client.get("/project/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Project Not Found"
