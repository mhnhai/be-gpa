from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.cohort import CohortResponse
from app.schemas.major import MajorResponse


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    cohort_id: Optional[int] = None
    major_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdateProfile(BaseModel):
    """Chỉ cho phép sửa email và họ tên."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    cohort: Optional[CohortResponse] = None
    major: Optional[MajorResponse] = None

    class Config:
        from_attributes = True
