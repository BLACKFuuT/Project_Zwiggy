from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ProfileBase(BaseModel):
    address: Optional[str] = None
    phone: Optional[str] = None


class ProfileResponse(ProfileBase):
    id: UUID

    class Config:
        from_attributes = True


# -------- USER SCHEMAS --------

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    address: Optional[str] = None
    phone: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    profile: Optional[ProfileResponse]

    class Config:
        from_attributes = True