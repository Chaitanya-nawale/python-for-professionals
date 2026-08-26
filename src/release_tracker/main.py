from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from .routers import projects

app = FastAPI(
    title="Release Tracker API",
    description="An API for tracking project milestones and developer tasks.",
)

app.include_router(projects.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Release Tracker API", "docs": "/docs"}


@app.exception_handler(IntegrityError)
def integrity_error_handler(request: Request, exp: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Data conflict occurred (e.g., duplicate entry)."},
    )
