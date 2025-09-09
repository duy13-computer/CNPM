# from domain.models.iauth_repository import IAuthRepository
# from domain.models.auth import Auth
# from typing import List, Optional
# from dotenv import load_dotenv
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from config import Config
# from sqlalchemy import Column, Integer, String, DateTime
# from infrastructure.databases import Base
# from sqlalchemy.orm import Session
# from infrastructure.databases.mssql import session
# from ..models.user_model import User
# load_dotenv()

# class AuthRepository(IAuthRepository):
#     def __init__(self, session: Session = session):
#         self._user = []
#         self._id_counter = 1
#         self.session = session

#     def login(self, auth: Auth) -> Auth:
#         return auth
#     def register(self, auth: Auth) -> Optional[Auth]:
#         auth.id = 1
#         return auth
#     def remember_password(self) -> Optional[Auth]:
#         return Auth()
#     def look_account(self, Id: int) -> bool:
#         return True
#     def un_look_account(self, watch_id: int) -> None:
#         return True
#     def check_exist(self, user_name: str) -> bool:
#         existing_user = self.session.query(User).filter_by(user_name = user_name).first()
#         if existing_user:
#            return False
#         return True
from domain.models.iauth_repository import IAuthRepository
from domain.models.auth import Auth
from typing import Optional
from infrastructure.databases.mssql import session
from domain.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
class AuthRepository(IAuthRepository):
    def __init__(self, session: Session = session):
        self.session = session

    def login(self, auth: Auth) -> Optional[Auth]:
        user = self.session.query(User).filter_by(user_name=auth.user_name).first()
        if user and check_password_hash(user.password, auth.password):
            return user
        return None

    def register(self, auth: Auth) -> Optional[Auth]:
        # Hash mật khẩu trước khi lưu
        from infrastructure.databases.mssql import session
        new_user = User(
            user_name=auth.user_name,
            password=generate_password_hash(auth.password),
            email=auth.email
        )
        session.add(new_user)
        session.commit()
        return new_user

    def check_exist(self, user_name: str) -> bool:
        existing_user = self.session.query(User).filter_by(user_name=user_name).first()
        return existing_user is not None
    def look_account(self, user_name: str):
        # ✅ Ví dụ: check user tồn tại
        return self.db.query(User).filter_by(user_name=user_name).first()

    def remember_password(self, user_id: int, new_password: str):
        # ✅ Ví dụ: update mật khẩu
        user = self.db.query(User).filter_by(user_id=user_id).first()
        if user:
            user.password = new_password
            self.db.commit()
        return user

    def un_look_account(self, user_id: int):
        # ✅ Ví dụ: unlock user account
        user = self.db.query(User).filter_by(user_id=user_id).first()
        if user:
            user.status = True
            self.db.commit()
        return user


