# app/infrastructure/refresh_token_repository_impl.py
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.models.refresh_token import RefreshToken
from app.domain.repositories.refresh_token_repository import IRefreshTokenRepository
from app.infrastructure.database import SessionLocal
import uuid

class RefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self):
        self.db: Session = SessionLocal()

    def create_refresh_token(self, token: RefreshToken) -> RefreshToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def get_refresh_token(self, token: str) -> Optional[RefreshToken]:
        return self.db.query(RefreshToken).filter(RefreshToken.token == token, RefreshToken.is_active == True).first()

    def revoke_refresh_token(self, token: str) -> None:
        refresh_token = self.get_refresh_token(token)
        if refresh_token:
            refresh_token.is_active = False
            self.db.commit()
            self.db.refresh(refresh_token)

    def revoke_all_tokens_for_user(self, user_id: uuid.UUID) -> None:
        tokens = self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id, RefreshToken.is_active == True).all()
        for token in tokens:
            token.is_active = False
        self.db.commit()
