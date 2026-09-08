from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.models.test import Test, TestRun  # Ensure SQLAlchemy models exist
from app.schemas.test import (
    TestCreate,
    TestResponse,
    TestRunCreate,
    TestRunResponse,
)
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/tests", tags=["Test Executions"])


@router.post("/", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
def create_test(
    test_data: TestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_test = Test(
        **test_data.model_dump(),
        created_by=current_user.id
    )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test


@router.get("/project/{project_id}", response_model=List[TestResponse])
def get_tests_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Test).filter(Test.project_id == project_id).all()


@router.post("/{test_id}/runs", response_model=TestRunResponse, status_code=status.HTTP_201_CREATED)
def submit_test_run(
    test_id: int,
    run_data: TestRunCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    new_run = TestRun(
        test_id=test_id,
        **run_data.model_dump(),
        executed_by=current_user.id
    )
    db.add(new_run)
    db.commit()
    db.refresh(new_run)
    return new_run


@router.get("/{test_id}/runs", response_model=List[TestRunResponse])
def get_test_runs(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    return db.query(TestRun).filter(TestRun.test_id == test_id).all()