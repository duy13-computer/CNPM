from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
import enum

class SellerVerification(enum.Enum):
    Pending = "Pending"
    Verified = "Verified"
    Rejected = "Rejected"

class Seller(Base):
    __tablename__ = "sellers"
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    seller_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total_sales = Column(Integer, default=0)
    verification_status = Column(Enum(SellerVerification), default=SellerVerification.Pending)

    # Relationships
    user = relationship("UserORM", backref="seller_profile")
    watches = relationship("Watch", back_populates="seller")
    transactions = relationship("Transaction", backref="seller") 