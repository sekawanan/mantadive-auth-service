# app/infrastructure/user_repository_impl.py
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.models.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.database import SessionLocal

class UserRepository(IUserRepository):
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        return self.db.query(User).filter(User.phone_number == phone_number).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User) -> None:
        self.db.commit()
        self.db.refresh(user)

    def delete_user(self, email: str) -> None:
        user = self.get_user_by_email(email)
        if user:
            self.db.delete(user)
            self.db.commit()
