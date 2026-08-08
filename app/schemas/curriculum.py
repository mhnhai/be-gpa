from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.catalog import CourseCatalogResponse
from app.schemas.major import MajorResponse


class CurriculumItemCreate(BaseModel):
    major_id: int
    course_catalog_id: int


class CurriculumBulkCreate(BaseModel):
    major_id: int
    course_catalog_ids: List[int]


class CurriculumItemResponse(BaseModel):
    id: int
    major_id: int
    course_catalog_id: int
    created_at: datetime
    course: Optional[CourseCatalogResponse] = None
    major: Optional[MajorResponse] = None

    class Config:
        from_attributes = True


class UserCurriculumResponse(BaseModel):
    """CTĐT đầy đủ của user = môn chung + môn ngành riêng"""

    major: Optional[MajorResponse] = None
    common_courses: List[CourseCatalogResponse]
    major_courses: List[CourseCatalogResponse]
    all_courses: List[CourseCatalogResponse]
