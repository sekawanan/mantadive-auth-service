# app/api/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas.user import UserCreate, UserOut, UserPhoneCreate
from app.use_cases.auth_use_cases import register_user, verify_email, forgot_password, reset_password, register_phone_user, login_user, oauth_callback
from app.use_cases.token_use_cases import refresh_access_token, revoke_refresh_token
from app.api.dependencies import get_user_repository, get_refresh_token_repository
from app.domain.repositories.user_repository import IUserRepository
from app.domain.repositories.refresh_token_repository import IRefreshTokenRepository
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest, LoginRequest, Token, TokenRefreshRequest, TokenRefreshResponse
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, 
            repo: IUserRepository = Depends(get_user_repository),
            refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    return register_user(user, repo, refresh_repo)

@router.post("/register/phone", response_model=UserOut)
def register_phone(user: UserPhoneCreate, 
                   repo: IUserRepository = Depends(get_user_repository),
                   refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    return register_phone_user(user, repo, refresh_repo)

@router.get("/verify-email")
def verify_email_endpoint(token: str, repo: IUserRepository = Depends(get_user_repository)):
    return verify_email(token, repo)

@router.post("/forgot-password")
def forgot_password_request(request: ForgotPasswordRequest, 
                            repo: IUserRepository = Depends(get_user_repository)):
    return forgot_password(request, repo)

@router.post("/reset-password")
def reset_password_request(request: ResetPasswordRequest, 
                           repo: IUserRepository = Depends(get_user_repository)):
    return reset_password(request, repo)

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), 
          repo: IUserRepository = Depends(get_user_repository),
          refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    return login_user(form_data, repo, refresh_repo)

@router.post("/refresh-token", response_model=TokenRefreshResponse)
def refresh_token_endpoint(request: TokenRefreshRequest, 
                           repo: IUserRepository = Depends(get_user_repository),
                           refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    tokens = refresh_access_token(request.refresh_token, repo, refresh_repo)
    return TokenRefreshResponse(**tokens)

@router.post("/logout")
def logout_endpoint(request: TokenRefreshRequest, 
                    refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    revoke_refresh_token(request.refresh_token, refresh_repo)
    return {"message": "Successfully logged out"}

@router.get("/auth/google")
def google_auth():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        "response_type=code&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        "scope=openid%20email%20profile&"
        "access_type=offline&"
        "prompt=consent"
    )
    return RedirectResponse(google_auth_url)

@router.get("/auth/google/callback", response_model=Token)
def google_callback(code: str, 
                   repo: IUserRepository = Depends(get_user_repository),
                   refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    try:
        user_out = oauth_callback(code, repo)
        tokens = issue_tokens(user_out, refresh_repo)
        return Token(**tokens)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
