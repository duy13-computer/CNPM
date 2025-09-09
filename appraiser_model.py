from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base


class Appraiser(Base):
    __tablename__ = "appraisers"
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    appraiser_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    specialization = Column(String(100))
    experience_years = Column(Integer)

    # Relationships
    user = relationship("UserORM", backref="appraiser_profile")
    appraisals = relationship("Appraisal", back_populates="appraiser")