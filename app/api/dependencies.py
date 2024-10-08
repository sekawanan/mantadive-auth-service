# app/api/dependencies.py
from app.infrastructure.user_repository_impl import UserRepository
from app.infrastructure.refresh_token_repository_impl import RefreshTokenRepository
from app.domain.repositories.user_repository import IUserRepository
from app.domain.repositories.refresh_token_repository import IRefreshTokenRepository

def get_user_repository() -> IUserRepository:
    return UserRepository()

def get_refresh_token_repository() -> IRefreshTokenRepository:
    return RefreshTokenRepository()
