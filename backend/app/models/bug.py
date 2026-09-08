# app/models/bug.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Bug(Base):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, default="medium")  # low, medium, high, critical
    status = Column(String, default="open")      # open, in_progress, resolved, closed
    failure_id = Column(Integer, ForeignKey("failures.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    failure = relationship("Failure", back_populates="bugs")
    analysis = relationship("Analysis", back_populates="bug", uselist=False, cascade="all, delete-orphan")