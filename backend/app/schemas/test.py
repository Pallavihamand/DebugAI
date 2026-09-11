
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TestBase(BaseModel):
    name: str
    description: Optional[str] = None


class TestCreate(TestBase):
    project_id: int


class TestResponse(TestBase):
    id: int
    project_id: int
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TestRunCreate(BaseModel):
    status: str  # passed, failed, error
    logs: Optional[str] = None


class TestRunResponse(BaseModel):
    id: int
    test_id: int
    status: str
    executed_by: int
    executed_at: datetime

    model_config = ConfigDict(from_attributes=True)

