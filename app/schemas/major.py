from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, field_validator, model_validator

MajorType = Literal["common", "specific"]


class MajorBase(BaseModel):
    name: str
    code: Optional[str] = None
    major_type: MajorType = "specific"
    description: Optional[str] = None
    cohort_id: Optional[int] = None
    is_active: bool = True

    @field_validator("major_type")
    @classmethod
    def validate_major_type(cls, value: str) -> str:
        if value not in ("common", "specific"):
            raise ValueError("major_type phải là 'common' hoặc 'specific'")
        return value

    @model_validator(mode="after")
    def validate_cohort_link(self):
        if self.major_type == "specific" and self.cohort_id is None:
            raise ValueError("Ngành riêng (specific) phải gắn cohort_id")
        if self.major_type == "common" and self.cohort_id is not None:
            raise ValueError("Ngành chung (common) không gắn cohort_id")
        return self


class MajorCreate(MajorBase):
    pass


class MajorUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    major_type: Optional[MajorType] = None
    description: Optional[str] = None
    cohort_id: Optional[int] = None
    is_active: Optional[bool] = None


class MajorResponse(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    major_type: MajorType
    description: Optional[str] = None
    cohort_id: Optional[int] = None
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True
