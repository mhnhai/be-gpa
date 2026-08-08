from typing import List

from pydantic import BaseModel


class CourseCatalogBase(BaseModel):
    course_code: str
    course_name: str
    credits: int


class CourseCatalogResponse(CourseCatalogBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class BulkAddCourses(BaseModel):
    semester_id: int
    course_ids: List[int]
    default_score: float = 0.0
