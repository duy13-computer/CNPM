from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.base import Base

class TodoModel(Base):
    __tablename__ = "todos"
    __table_args__ = {'extend_existing': True}  # Allow extending existing table

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)