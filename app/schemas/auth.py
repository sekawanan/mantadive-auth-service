from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: str = Field(..., min_length=6)

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class TokenRefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class ForgotPasswordRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class ResendVerificationEmailRequest(BaseModel):
    email: EmailStr
