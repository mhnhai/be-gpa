from typing import List

from pydantic import BaseModel

from app.schemas.semester import SemesterWithGPA


class GPASummary(BaseModel):
    cumulative_gpa: float
    total_credits: int
    total_courses: int
    semesters: List[SemesterWithGPA]
