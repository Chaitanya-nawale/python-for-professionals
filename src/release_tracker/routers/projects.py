from fastapi import APIRouter, status
from fastapi.responses import Response

from .. import crud
from ..dependencies import ProjectDep, SessionDep
from ..models import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectRead])
def list_projects(session: SessionDep):
    return crud.list_projects(session)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project: ProjectDep, session: SessionDep):
    return project


@router.post(
    "/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED
)
def projectCreate(payload: ProjectCreate, session: SessionDep):
    project = crud.create_project(session, payload)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def projectDelete(project: ProjectDep, session: SessionDep):
    crud.delete_project(session, project)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
)
def projectUpdate(
    project: ProjectDep, payload: ProjectUpdate, session: SessionDep
):
    crud.update_project(session, project, payload)
    return project


# @app.get("/async", response_model=list[ProjectRead])
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


# @app.get("/name", response_model=list[ProjectRead])
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
