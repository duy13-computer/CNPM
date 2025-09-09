# from infrastructure.repositories.user_repository import IUserRepository
# from werkzeug.security import generate_password_hash, check_password_hash
# from typing import Optional

# class UserService:
#     def __init__(self, user_repository: IUserRepository):
#         self.user_repository = user_repository

#     def create_user(self, user_name: str, password: str, description: Optional[str], status: bool):
#         # Check user tồn tại chưa
#         existing_user = self.user_repository.get_by_username(user_name)
#         if existing_user:
#             raise ValueError("Username already exists")

#         hashed_pw = generate_password_hash(password)
#         return self.user_repository.create(user_name, hashed_pw, description, status)

#     def authenticate_user(self, user_name: str, password: str):
#         user = self.user_repository.get_by_username(user_name)
#         if not user:
#             return None
#         if not check_password_hash(user.password, password):
#             return None
#         return user

#     def list_users(self):
#         return self.user_repository.get_all()

#     def get_user(self, user_id: int):
#         return self.user_repository.get_by_id(user_id)
#     def update_user(self, user_id: int, user_name: str, password: Optional[str], description: Optional[str], status: bool):
#         user = self.user_repository.get_by_id(user_id)
#         if not user:
#             raise ValueError("User not found")

#         if password:
#             hashed_pw = generate_password_hash(password)
#         else:
#             hashed_pw = user.password
#         return self.user_repository.update(user_id, user_name, hashed_pw, description, status)
#     def delete_user(self, user_id: int):
#         user = self.user_repository.get_by_id(user_id)
#         if not user:
#             raise ValueError("User not found")
#         return self.user_repository.delete(user_id)

from infrastructure.repositories.user_repository import IUserRepository
from domain.models.user import User, UserRole
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def create_user(self, user_name: str, email: str, password: str, role: UserRole):
        # Kiểm tra user_name đã tồn tại chưa
        existing_user = self.user_repository.get_by_username(user_name)
        if existing_user:
            raise ValueError("Username already exists")

        # Kiểm tra email đã tồn tại chưa
        existing_email = self.user_repository.get_by_email(email)
        if existing_email:
            raise ValueError("Email already exists")

        hashed_pw = generate_password_hash(password)
        new_user = User(
            user_name=user_name,
            email=email,
            password=hashed_pw,
            role=role
        )
        return self.user_repository.add(new_user)

    def authenticate_user(self, user_name: str, password: str) -> Optional[User]:
        user = self.user_repository.get_by_username(user_name)
        if not user:
            return None
        if not check_password_hash(user.password, password):
            return None
        return user

    def list_users(self):
        return self.user_repository.list()

    def get_user(self, user_id: int):
        return self.user_repository.get_by_id(user_id)

    def update_user(self, user_id: int, user_name: str, email: str, password: Optional[str], role: UserRole):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if password:
            hashed_pw = generate_password_hash(password)
        else:
            hashed_pw = user.password

        user.user_name = user_name
        user.email = email
        user.password = hashed_pw
        user.role = role

        return self.user_repository.update(user)

    def delete_user(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return self.user_repository.delete(user_id)
