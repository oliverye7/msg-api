from pydantic import BaseModel, EmailStr
from app.models.user import AuthProvider
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    auth_provider: AuthProvider
    provider_user_id: str

class User(UserBase):
    id: int
    auth_provider: AuthProvider
    is_active: bool
    created_at: datetime
    updated_at: datetime
    api_key: Optional[str] = None

    class Config:
        from_attributes = True