from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
from datetime import datetime


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = {'extend_existing': True}  # Allow extending existing table

    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    from_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rating = Column(Integer, CheckConstraint("rating BETWEEN 1 AND 5"), nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    from_user = relationship("UserORM", foreign_keys=[from_user_id], backref="feedback_given")
    to_user = relationship("UserORM", foreign_keys=[to_user_id], backref="feedback_received")