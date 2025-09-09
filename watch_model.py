from sqlalchemy import Column, Integer, String, DECIMAL, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
import enum

class WatchStatus(enum.Enum):
    Listed = "Listed"
    Sold = "Sold"
    Withdrawn = "Withdrawn"
    Pending_appraisal = "Pending_appraisal"

class Watch(Base):
    __tablename__ = "watches"
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    watch_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("sellers.seller_id"), nullable=False)
    title = Column(String(150), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer)
    description = Column(Text)
    status = Column(Enum(WatchStatus), default=WatchStatus.Listed)
    price = Column(DECIMAL(12, 2), nullable=False)

    # Relationships
    seller = relationship("Seller", back_populates="watches")
    transactions = relationship("Transaction", back_populates="watch")