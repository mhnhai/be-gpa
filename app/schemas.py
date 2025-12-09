from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ============ Course Catalog Schemas ============
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


# ============ User Schemas ============
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ============ Course Schemas ============
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


# ============ Semester Schemas ============
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


# ============ GPA Summary Schemas ============
class GPASummary(BaseModel):
    cumulative_gpa: float
    total_credits: int
    total_courses: int
    semesters: List[SemesterWithGPA]

