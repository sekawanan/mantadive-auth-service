# app/use_cases/auth_use_cases.py
from datetime import timedelta
from fastapi import HTTPException, status
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import PhoneRegister
from app.domain.repositories.user_repository import IUserRepository
from app.domain.models.user import User
from app.core.security import get_password_hash, create_access_token, decode_access_token
from app.infrastructure.smtp import send_verification_email, send_password_reset_email
from app.infrastructure.whatsapp import send_whatsapp_verification, send_whatsapp_password_reset
from app.infrastructure.google_oauth import get_google_user_info, get_google_oauth_token

def register_user(user_create: UserCreate, repo: IUserRepository) -> UserOut:
    existing_user = repo.get_user_by_email(user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = repo.get_user_by_username(user_create.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
        full_name=user_create.full_name,
        is_active=True  # User is active but not verified
    )
    created_user = repo.create_user(user)
    send_verification_email(created_user.email, created_user.username)
    return UserOut.from_orm(created_user)

def register_phone_user(user_create: PhoneRegister, repo: IUserRepository) -> UserOut:
    existing_user = repo.get_user_by_phone(user_create.phone_number)
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    existing_username = repo.get_user_by_username(user_create.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        username=user_create.username,
        phone_number=user_create.phone_number,
        full_name=user_create.full_name,
        is_active=True  # User is active but not verified
    )
    created_user = repo.create_user(user)
    send_whatsapp_verification(created_user.phone_number, created_user.username)
    return UserOut.from_orm(created_user)

def oauth_callback(code: str, repo: IUserRepository) -> UserOut:
    token = get_google_oauth_token(code)
    user_info = get_google_user_info(token)
    user = repo.get_user_by_email(user_info["email"])
    if not user:
        user = User(
            username=user_info["email"],
            email=user_info["email"],
            full_name=user_info.get("name"),
            is_active=True,
            is_verified=True
        )
        user = repo.create_user(user)
    access_token = create_access_token(data={"sub": user.username})
    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name
    )

def verify_email(token: str, repo: IUserRepository) -> dict:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    username = payload.get("sub")
    user = repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        return {"message": "Email already verified"}
    user.is_verified = True
    repo.update_user(user)
    return {"message": "Email verified successfully"}

def forgot_password(request, repo: IUserRepository) -> dict:
    user = None
    if request.email:
        user = repo.get_user_by_email(request.email)
    elif request.phone_number:
        user = repo.get_user_by_phone(request.phone_number)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(hours=1))
    if user.email:
        send_password_reset_email(user.email, token)
    if user.phone_number:
        send_whatsapp_password_reset(user.phone_number, token)

    return {"message": "Password reset instructions sent"}

def reset_password(request, repo: IUserRepository) -> dict:
    payload = decode_access_token(request.token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    username = payload.get("sub")
    user = repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(request.new_password)
    repo.update_user(user)
    return {"message": "Password reset successfully"}
