from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base


class Admin(Base):
    __tablename__ = "admin"
    __table_args__ = {'extend_existing': True}  # Allow extending existing table

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20))

    can_manage_products = Column(Boolean, default=True)
    can_manage_users = Column(Boolean, default=True)

    # Relationships
    user = relationship("UserORM", backref="admin_profile")