# app/domain/repositories/refresh_token_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.refresh_token import RefreshToken
import uuid

class IRefreshTokenRepository(ABC):
    @abstractmethod
    def create_refresh_token(self, token: RefreshToken) -> RefreshToken:
        pass

    @abstractmethod
    def get_refresh_token(self, token: str) -> Optional[RefreshToken]:
        pass

    @abstractmethod
    def revoke_refresh_token(self, token: str) -> None:
        pass

    @abstractmethod
    def revoke_all_tokens_for_user(self, user_id: uuid.UUID) -> None:
        pass
