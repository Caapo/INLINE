from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    def save_user(self, user:User) -> None:
        pass

    @abstractmethod
    def find_user_by_email(self, email:str) -> Optional[User]:
        pass