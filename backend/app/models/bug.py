from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Bug(Base):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)
    failure_id = Column(Integer, ForeignKey("failures.id"))
    title = Column(String, nullable=False)
    severity = Column(String, default="medium")  # low, medium, high, critical
    status = Column(String, default="open")      # open, resolved, closed
    created_at = Column(DateTime, default=datetime.utcnow)

    failure = relationship("Failure", back_populates="bugs")
    analyses = relationship("Analysis", back_populates="bug")