from fastapi import FastAPI

app = FastAPI(title="Release Tracker API")

@app.get("/projects")
def list_projects() -> list[dict]:
    """
    List all projects in the release tracker.
    """
    return [
        {"id": 1, "name": "Project A"},
        {"id": 2, "name": "Project B"},
        {"id": 3, "name": "Project C"},
    ]
