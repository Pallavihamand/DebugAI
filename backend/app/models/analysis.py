from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    bug_id = Column(Integer, ForeignKey("bugs.id"))
    root_cause = Column(Text, nullable=False)
    suggested_fix = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bug = relationship("Bug", back_populates="analyses")