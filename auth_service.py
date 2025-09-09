import jwt
from typing import List, Optional
from domain.models.auth import Auth
from domain.models.iauth_repository import IAuthRepository

class AuthService:
    def __init__(self, repository: IAuthRepository):
        self.repository = repository
    def register(self, user_name: str, password: str, email: str) -> Optional[Auth]:
        if self.repository.check_exist(user_name):
            return None
        auth = Auth(user_name=user_name, password=password, email=email, password_confirm=password)
        return self.repository.register(auth)
    def login(self, user_name: str, password: str) -> Optional[Auth]:
        auth = Auth(user_name=user_name, password=password, email="", password_confirm=password)
        return self.repository.login(auth)
    def remember_password(self) -> Optional[Auth]:
        return self.repository.remember_password()
    def look_account(self, Id: int) -> bool:
        return self.repository.look_account(Id)
    def un_look_account(self, watch_id: int) -> None:
        return self.repository.un_look_account(watch_id)
    def check_exist(self, user_name: str) -> bool:
        return self.repository.check_exist(user_name)
