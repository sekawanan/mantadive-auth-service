# app/use_cases/token_use_cases.py
from datetime import timedelta, datetime
from typing import Dict
from fastapi import HTTPException, status
from app.core.security import create_access_token, create_refresh_token, decode_refresh_token
from app.domain.repositories.refresh_token_repository import IRefreshTokenRepository
from app.domain.repositories.user_repository import IUserRepository
from app.domain.models.refresh_token import RefreshToken
from app.domain.models.user import User
from app.core.config import settings
import uuid

def issue_tokens(user: User, refresh_repo: IRefreshTokenRepository) -> Dict[str, str]:
    access_token = create_access_token(data={"user_id": str(user.id), "username": user.username})
    refresh_token_str = create_refresh_token(data={"user_id": str(user.id), "username": user.username})
    
    refresh_token = RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    refresh_repo.create_refresh_token(refresh_token)
    
    return {"access_token": access_token, "refresh_token": refresh_token_str}

def refresh_access_token(refresh_token: str, user_repo: IUserRepository, refresh_repo: IRefreshTokenRepository) -> Dict[str, str]:
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    username = payload.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token payload")
    user = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # Verify refresh token exists and is active
    stored_refresh_token = refresh_repo.get_refresh_token(refresh_token)
    if not stored_refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found or inactive")
    # Optionally: Check if refresh token is expired based on expires_at
    if stored_refresh_token.expires_at < datetime.utcnow():
        refresh_repo.revoke_refresh_token(refresh_token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    # Issue new tokens
    tokens = issue_tokens(user, refresh_repo)
    # Revoke the old refresh token
    refresh_repo.revoke_refresh_token(refresh_token)
    return tokens

def revoke_refresh_token(refresh_token: str, refresh_repo: IRefreshTokenRepository) -> None:
    refresh_repo.revoke_refresh_token(refresh_token)

def revoke_all_user_tokens(user: User, refresh_repo: IRefreshTokenRepository) -> None:
    refresh_repo.revoke_all_tokens_for_user(user.id)
