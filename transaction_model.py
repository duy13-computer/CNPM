from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
import enum
from datetime import datetime

class PaymentStatus(enum.Enum):
    Pending = "Pending"
    Paid = "Paid"
    Refunded = "Refunded"

class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {'extend_existing': True}  # Allow extending existing table

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    watch_id = Column(Integer, ForeignKey("watches.watch_id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("buyers.buyer_id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.seller_id"), nullable=False)
    price_final = Column(DECIMAL(12, 2), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.Pending)
    feedback_left = Column(Boolean, default=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    watch = relationship("Watch", back_populates="transactions")
    buyer = relationship("Buyer", back_populates="transactions")