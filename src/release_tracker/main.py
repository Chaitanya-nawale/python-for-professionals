import asyncio

from fastapi import FastAPI, HTTPException, status
from pydantic.main import BaseModel

app = FastAPI(title="Release Tracker API")


class ProjectRead(BaseModel):
    id: int
    name: str
    slug: str


@app.get("/project/{project_id}", response_model=ProjectRead)
def get_project(project_id: int) -> ProjectRead:
    project = mock_projects_db.get(project_id, None)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project Not Found"
        )
    return mock_projects_db[project_id]


@app.get("/projects/async", response_model=list[ProjectRead])
async def list_projects_async(
    project_name: str | None = None,
) -> list[ProjectRead]:
    await asyncio.sleep(1)
    if project_name:
        return [
            project
            for project in mock_projects_db.values()
            if project.name == project_name
        ]
    return list(mock_projects_db.values())


@app.get("/projects/name", response_model=list[ProjectRead])
def list_projects_with_name(
    project_name: str | None = None,
) -> list[ProjectRead]:
    if project_name:
        return [
            project
            for project in mock_projects_db.values()
            if project.name == project_name
        ]
    return list(mock_projects_db.values())


@app.get("/projects", response_model=list[ProjectRead])
def list_projects_with_slug(
    project_slug: str | None = None,
) -> list[ProjectRead]:
    if project_slug:
        return [
            project
            for project in mock_projects_db.values()
            if project.slug == project_slug
        ]
    return list(mock_projects_db.values())


mock_projects_db: dict[int, ProjectRead] = {
    1: ProjectRead(id=1, name="Project A", slug="project-a"),
    2: ProjectRead(id=2, name="Project B", slug="project-b"),
    3: ProjectRead(id=3, name="Project C", slug="project-c"),
}
