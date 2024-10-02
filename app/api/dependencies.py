from app.infrastructure.user_repository_impl import UserRepository
from app.domain.repositories.user_repository import IUserRepository

def get_user_repository() -> IUserRepository:
    return UserRepository()
