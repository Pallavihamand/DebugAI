from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class TestBase(BaseModel):
    title: str
    file_path: str
    framework: str

class TestCreate(TestBase):
    project_id: int

class TestResponse(TestBase):
    id: int
    project_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TestRunCreate(BaseModel):
    test_id: int
    status: str  # passed, failed, error
    logs: Optional[str] = None

class TestRunResponse(BaseModel):
    id: int
    test_id: int
    status: str
    logs: Optional[str] = None
    executed_at: datetime

    model_config = ConfigDict(from_attributes=True)