from abc import ABC, abstractmethod
from .auth import Auth
from typing import List, Optional

class IAuthRepository(ABC):
    @abstractmethod
    def login(self, auth: Auth) -> Auth:
        pass

    @abstractmethod
    def register(self, auth: Auth) -> Optional[Auth]:
        pass

    @abstractmethod
    def remember_password(self) -> Optional[Auth]:
        pass

    @abstractmethod
    def look_account(self, Id: int) -> bool:
        pass

    @abstractmethod
    def un_look_account(self, watch_id: int) -> None:
        pass

    @abstractmethod
    def check_exist(self, user_name: str) -> bool:
        pass
