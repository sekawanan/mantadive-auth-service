# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    # full_name: Optional[str] = None

class UserPhoneCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    phone_number: str
    password: str = Field(..., min_length=6)
    # full_name: str
    
class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    email: Optional[EmailStr]
    # full_name: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True
