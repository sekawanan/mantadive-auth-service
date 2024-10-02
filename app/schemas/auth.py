# app/schemas/auth.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: str

class PhoneRegister(BaseModel):
    username: Optional[str]
    phone_number: str
    full_name: Optional[str] = None

class ForgotPasswordRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
