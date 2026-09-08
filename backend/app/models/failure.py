# app/models/failure.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Failure(Base):
    __tablename__ = "failures"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    error_type = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    stack_trace = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Make sure back_populates matches the property name in Test ("failures")
    test = relationship("Test", back_populates="failures")
    bugs = relationship("Bug", back_populates="failure", cascade="all, delete-orphan")