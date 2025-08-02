from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    gender: Optional[str] = None
    age: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserTokens(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token_expiry: Optional[datetime] = None
    refresh_token_expiry: Optional[datetime] = None

class UserOut(UserCreate, UserTokens):
    id: int

    class Config:
        from_attributes = True  # ✅ Updated for Pydantic v2 compatibility
