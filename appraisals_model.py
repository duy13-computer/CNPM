from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
import enum
from datetime import datetime


class Authenticity(enum.Enum):
    Authentic = "Authentic"
    Fake = "Fake"
    Unverified = "Unverified"


class Appraisal(Base):
    __tablename__ = "appraisals"
    __table_args__ = {'extend_existing': True}  # Allow extending existing table

    appraisal_id = Column(Integer, primary_key=True, autoincrement=True)
    watch_id = Column(Integer, ForeignKey("watches.watch_id"), nullable=False)
    appraiser_id = Column(Integer, ForeignKey("appraisers.appraiser_id"), nullable=False)
    authenticity = Column(Enum(Authenticity), default=Authenticity.Unverified)
    condition_notes = Column(Text)
    report_document = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    watch = relationship("Watch", backref="appraisals")
    appraiser = relationship("Appraiser", back_populates="appraisals")