from app.database.connection import Base

# Import all models to register them with Base.metadata
from app.models.user import User
from app.models.project import Project
from app.models.test import Test, TestRun
from app.models.failure import Failure
from app.models.bug import Bug
from app.models.analysis import Analysis

__all__ = [
    "Base",
    "User",
    "Project",
    "Test",
    "TestRun",
    "Failure",
    "Bug",
    "Analysis",
]