from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlmodel import Session

from . import crud
from .database import get_session
from .models import Project, ProjectCreate, ProjectRead, ProjectUpdate

app = FastAPI(
    title="Release Tracker API",
    description="An API for tracking project milestones and developer tasks.",
)


SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Release Tracker API", "docs": "/docs"}


@app.get("/projects", response_model=list[ProjectRead])
def list_projects(session: SessionDep):
    return crud.list_projects(session)


def findProjectInDB(session: SessionDep, project_id: int) -> Project:
    project = crud.get_project(session, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project Not Found"
        )
    return project


@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: SessionDep):
    project = findProjectInDB(session, project_id)
    return project


@app.post(
    "/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED
)
def projectCreate(payload: ProjectCreate, session: SessionDep):
    project = crud.create_project(session, payload)
    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def projectDelete(project_id: int, session: SessionDep):
    project = findProjectInDB(session, project_id)
    crud.delete_project(session, project)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch(
    "/projects/{project_id}",
    response_model=ProjectRead,
)
def projectUpdate(project_id: int, payload: ProjectUpdate, session: SessionDep):
    project = findProjectInDB(session, project_id)
    crud.update_project(session, project, payload)
    return project


# @app.get("/projects/async", response_model=list[ProjectRead])
# async def list_projects_async(
#     project_name: str | None = None,
# ) -> list[ProjectRead]:
#     await asyncio.sleep(1)
#     if project_name:
#         return [
#             project
#             for project in mock_projects_db.values()
#             if project.name == project_name
#         ]
#     return list(mock_projects_db.values())


# @app.get("/projects/name", response_model=list[ProjectRead])
# def list_projects_with_name(
#     project_name: str | None = None,
# ) -> list[ProjectRead]:
#     if project_name:
#         return [
#             project
#             for project in mock_projects_db.values()
#             if project.name == project_name
#         ]
#     return list(mock_projects_db.values())
