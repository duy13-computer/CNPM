from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, Enum, DateTime
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
from datetime import datetime
import enum


class PaymentStatus(enum.Enum):
    Pending = "Pending"
    Completed = "Completed"
    Failed = "Failed"
    Paid = "Paid"
    Refunded = "Refunded"


class Payment(Base):
    __tablename__ = "payment"
    __table_args__ = {'extend_existing': True}  # Allow extending existing table

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.Pending)

    # Relationships
    transaction = relationship("Transaction", backref="payments")