# from domain.models.iuser_repository import IUserRepository
# from domain.models.todo import Todo
# from typing import List, Optional
# from dotenv import load_dotenv
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from config import Config
# from sqlalchemy import Column, Integer, String, DateTime
# from infrastructure.databases import Base
# from sqlalchemy.orm import Session
# from infrastructure.models.user_model import User
# from infrastructure.databases.mssql import session

# load_dotenv()

# class UserRepository(IUserRepository):
#     def __init__(self, session: Session = session):
#         self.session = session

#     def add(self, user: User) -> User:
#         try:
#             self.session.add(user)
#             self.session.commit()
#             self.session.refresh(user)
#             return user
#         except Exception as e:
#             self.session.rollback()
#             raise ValueError('User not found')
#         finally:
#             self.session.close()

#     def get_by_id(self, user_id: int) -> Optional[User]:
#         return self.session.query(User).filter_by(id=user_id).first()

#     def get_by_username(self, user_name: str) -> Optional[User]:
#         return self.session.query(User).filter_by(user_name=user_name).first()

#     def list(self) -> List[User]:
#         return self.session.query(User).all()
from domain.models.iuser_repository import IUserRepository
from infrastructure.models.user_model import UserORM
from domain.models.user import User

class UserRepository(IUserRepository):
    def __init__(self, db_session):
        self.db = db_session

    def get_by_username(self, username: str):
        record = self.db.query(UserORM).filter(UserORM.user_name == username).first()
        if record:
            return User(
                user_id=record.user_id,
                user_name=record.user_name,
                email=record.email,
                password=record.password,
                role=record.role
            )
        return None
    
    def get_by_email(self, email: str):
        record = self.db.query(UserORM).filter(UserORM.email == email).first()
        if record:
            return User(
                user_id=record.user_id,
                user_name=record.user_name,
                email=record.email,
                password=record.password,
                role=record.role
            )
        return None

    def add(self, user: User):
        record = UserORM(
            user_name=user.user_name,
            email=user.email,
            password=user.password,
            role=user.role
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return User(
            user_id=record.user_id,
            user_name=record.user_name,
            email=record.email,
            password=record.password,
            role=record.role
        )
    # 🟢 Bổ sung các method bắt buộc
    def get_by_id(self, user_id: int):
        record = self.db.query(UserORM).filter(UserORM.user_id == user_id).first()
        if record:
            return User(
                user_id=record.user_id,
                user_name=record.user_name,
                email=record.email,
                password=record.password,
                role=record.role
            )
        return None

    def list(self):
        records = self.db.query(UserORM).all()
        return [
            User(
                user_id=r.user_id,
                user_name=r.user_name,
                email=r.email,
                password=r.password,
                role=r.role
            ) for r in records
        ]

    def update(self, user: User):
        record = self.db.query(UserORM).filter(UserORM.user_id == user.user_id).first()
        if not record:
            return None
        record.user_name = user.user_name
        record.email = user.email
        record.password = user.password
        record.role = user.role
        self.db.commit()
        self.db.refresh(record)
        return User(
            user_id=record.user_id,
            user_name=record.user_name,
            email=record.email,
            password=record.password,
            role=record.role
        )

    def delete(self, user_id: int):
        record = self.db.query(UserORM).filter(UserORM.user_id == user_id).first()
        if record:
            self.db.delete(record)
            self.db.commit()
            return True
        return False


