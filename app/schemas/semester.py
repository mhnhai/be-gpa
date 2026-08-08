from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.course import CourseResponse


class SemesterBase(BaseModel):
    name: str
    year: int
    semester_number: int


class SemesterCreate(SemesterBase):
    pass


class SemesterUpdate(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None
    semester_number: Optional[int] = None


class SemesterResponse(SemesterBase):
    id: int
    user_id: int
    created_at: datetime
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True


class SemesterWithGPA(SemesterResponse):
    semester_gpa: float
    total_credits: int
