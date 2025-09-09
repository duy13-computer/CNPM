from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class Buyer(Base):
    __tablename__ = "buyers"
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    buyer_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    purchase_history_count = Column(Integer, default=0)

    # Relationships
    user = relationship("UserORM", backref="buyer_profile")
    transactions = relationship("Transaction", back_populates="buyer")
    