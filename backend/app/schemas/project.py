from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    name: str
    repo_path: str


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

