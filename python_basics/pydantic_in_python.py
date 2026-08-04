from pydantic import BaseModel, Field


class Project(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=100, description="The name of the project"
    )
    description: str | None = Field(
        None, description="A brief description of the project", max_length=500
    )
