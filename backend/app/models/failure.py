from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Failure(Base):
    __tablename__ = "failures"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    test_run_id = Column(Integer, ForeignKey("test_runs.id"))
    error_message = Column(Text, nullable=False)
    traceback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    test = relationship("Test", back_populates="failures")
    test_run = relationship("TestRun", back_populates="failures")
    bugs = relationship("Bug", back_populates="failure")