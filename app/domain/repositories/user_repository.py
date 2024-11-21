from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.user import User

class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> None:
        pass

    @abstractmethod
    def delete_user(self, email: str) -> None:
        pass
