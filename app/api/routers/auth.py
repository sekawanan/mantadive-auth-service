from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas.user import UserCreate, UserOut
from app.use_cases.auth_use_cases import register_user, verify_email, forgot_password, reset_password, register_phone_user, oauth_callback
from app.api.dependencies import get_user_repository
from app.domain.repositories.user_repository import IUserRepository
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest, PhoneRegister, LoginRequest, Token
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, repo: IUserRepository = Depends(get_user_repository)):
    return register_user(user, repo)

@router.post("/register/phone", response_model=UserOut)
def register_phone(user: PhoneRegister, repo: IUserRepository = Depends(get_user_repository)):
    return register_phone_user(user, repo)

@router.get("/verify-email")
def verify_email_endpoint(token: str, repo: IUserRepository = Depends(get_user_repository)):
    return verify_email(token, repo)

@router.post("/forgot-password")
def forgot_password_request(request: ForgotPasswordRequest, repo: IUserRepository = Depends(get_user_repository)):
    return forgot_password(request, repo)

@router.post("/reset-password")
def reset_password_request(request: ResetPasswordRequest, repo: IUserRepository = Depends(get_user_repository)):
    return reset_password(request, repo)

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), repo: IUserRepository = Depends(get_user_repository)):
    user = repo.get_user_by_username(form_data.username)
    if not user:
        user = repo.get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Unverified user")
    from app.core.security import verify_password
    if not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

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
def google_callback(code: str, repo: IUserRepository = Depends(get_user_repository)):
    try:
        user_out = oauth_callback(code, repo)
        access_token = create_access_token(data={"sub": user_out.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
