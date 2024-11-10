from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserOut, UserPhoneCreate
from app.use_cases.auth_use_cases import register_user, verify_email, forgot_password, reset_password, register_phone_user, login_user, oauth_callback, resend_verification_email
from app.use_cases.token_use_cases import refresh_access_token, revoke_refresh_token, issue_tokens
from app.api.dependencies import get_user_repository, get_refresh_token_repository
from app.domain.repositories.user_repository import IUserRepository
from app.domain.repositories.refresh_token_repository import IRefreshTokenRepository
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest, LoginRequest, Token, TokenRefreshRequest, TokenRefreshResponse, ResendVerificationEmailRequest
from app.utils.responses import create_success_response, create_error_response
from fastapi.responses import RedirectResponse
from app.core.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.base_response import BaseResponse, ErrorDetail

router = APIRouter()

@router.post("/register", response_model=BaseResponse[UserOut])
def register(user: UserCreate, 
            repo: IUserRepository = Depends(get_user_repository),
            refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    try:
        created_user = register_user(user, repo, refresh_repo)
        return create_success_response(created_user)
    except HTTPException as e:       
        raise e

@router.post("/register/phone", response_model=BaseResponse[UserOut])
def register_phone(user: UserPhoneCreate, 
                   repo: IUserRepository = Depends(get_user_repository),
                   refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    try:
        created_user = register_phone_user(user, repo, refresh_repo)
        return create_success_response(created_user)
    except HTTPException as e:
        raise e

@router.get("/verify-email", response_model=BaseResponse[dict])
def verify_email_endpoint(token: str, repo: IUserRepository = Depends(get_user_repository)):
    try:
        message = verify_email(token, repo)
        return create_success_response({"message": message})
    except HTTPException as e:
        raise e

@router.post("/forgot-password", response_model=BaseResponse[dict])
def forgot_password_request(request: ForgotPasswordRequest, 
                            repo: IUserRepository = Depends(get_user_repository)):
    try:
        message = forgot_password(request, repo)
        return create_success_response({"message": message})
    except HTTPException as e:
        raise e

@router.post("/reset-password", response_model=BaseResponse[dict])
def reset_password_request(request: ResetPasswordRequest, 
                           repo: IUserRepository = Depends(get_user_repository)):
    try:
        message = reset_password(request, repo)
        return create_success_response({"message": message})
    except HTTPException as e:
        raise e

@router.post("/token", response_model=BaseResponse[Token])
def login(form_data: OAuth2PasswordRequestForm = Depends(), 
          repo: IUserRepository = Depends(get_user_repository),
          refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    try:
        token = login_user(form_data, repo, refresh_repo)
        return create_success_response(token)
    except HTTPException as e:
        raise e

@router.post("/refresh-token", response_model=BaseResponse[TokenRefreshResponse])
def refresh_token_endpoint(request: TokenRefreshRequest, 
                           repo: IUserRepository = Depends(get_user_repository),
                           refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    try:
        tokens = refresh_access_token(request.refresh_token, repo, refresh_repo)
        response = TokenRefreshResponse(**tokens)
        return create_success_response(response)
    except HTTPException as e:
        raise e

@router.post("/logout", response_model=BaseResponse[dict])
def logout_endpoint(request: TokenRefreshRequest, 
                    refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    try:
        revoke_refresh_token(request.refresh_token, refresh_repo)
        return create_success_response({"message": "Successfully logged out"})
    except HTTPException as e:
        raise e

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

@router.get("/auth/google/callback", response_model=BaseResponse[Token])
def google_callback(code: str, 
                   repo: IUserRepository = Depends(get_user_repository),
                   refresh_repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)):
    try:
        user_out = oauth_callback(code, repo)
        tokens = issue_tokens(user_out, refresh_repo)
        return create_success_response(tokens)
    except HTTPException as e:
        return create_error_response(e.status_code, e.detail)
    except Exception as e:
        raise e
    
@router.post("/resend-verification-email", response_model=BaseResponse[dict])
def resend_verification_email_endpoint(
    request: ResendVerificationEmailRequest,
    repo: IUserRepository = Depends(get_user_repository)
):
    """
    Endpoint to resend the verification email to the user.
    """
    try:
        message = resend_verification_email(request.email, repo)
        return create_success_response({"message": message})
    except HTTPException as e:
        raise e
