from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

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
    full_name: Optional[str] = None
    cohort_id: Optional[int] = None
    major_id: Optional[int] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    cohort: Optional[CohortResponse] = None
    major: Optional[MajorResponse] = None

    class Config:
        from_attributes = True
