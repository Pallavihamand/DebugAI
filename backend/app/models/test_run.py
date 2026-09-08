from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(String, default="pending")  # pending, running, completed, failed
    executed_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="test_runs")
    failures = relationship("Failure", back_populates="test_run")