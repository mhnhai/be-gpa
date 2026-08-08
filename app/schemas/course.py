from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    course_code: str
    course_name: str
    credits: int
    score: float


class CourseCreate(CourseBase):
    semester_id: int


class CourseUpdate(BaseModel):
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    credits: Optional[int] = None
    score: Optional[float] = None


class CourseResponse(CourseBase):
    id: int
    letter_grade: Optional[str]
    grade_point: Optional[float]
    semester_id: int
    created_at: datetime

    class Config:
        from_attributes = True
