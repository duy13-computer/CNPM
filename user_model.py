from sqlalchemy import Column, Integer, String, Enum
from infrastructure.databases.base import Base
from domain.models.user import UserRole


class UserORM(Base):
    __tablename__ = "users"   
    __table_args__ = {'extend_existing': True}  

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(225), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
