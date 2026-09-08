from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class FailureCreate(BaseModel):
    test_run_id: int
    error_message: str
    stack_trace: Optional[str] = None

class FailureResponse(BaseModel):
    id: int
    test_run_id: int
    error_message: str
    stack_trace: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class BugResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    suggested_fix: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnalysisResponse(BaseModel):
    id: int
    failure_id: int
    root_cause: str
    confidence_score: float
    recommendation: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)