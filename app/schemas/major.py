from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, field_validator

MajorType = Literal["common", "specific"]


class MajorBase(BaseModel):
    name: str
    code: Optional[str] = None
    major_type: MajorType = "specific"
    description: Optional[str] = None
    is_active: bool = True

    @field_validator("major_type")
    @classmethod
    def validate_major_type(cls, value: str) -> str:
        if value not in ("common", "specific"):
            raise ValueError("major_type phải là 'common' hoặc 'specific'")
        return value


class MajorCreate(MajorBase):
    pass


class MajorUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    major_type: Optional[MajorType] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class MajorResponse(MajorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
