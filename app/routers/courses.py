from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.crud import course as course_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate

router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Thêm môn học mới vào học kỳ"""
    db_course = course_crud.create_course(db, course, current_user.id)
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học kỳ hoặc bạn không có quyền thêm môn học",
        )
    return db_course


@router.get("/semester/{semester_id}", response_model=List[CourseResponse])
def get_courses_by_semester(
    semester_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy danh sách môn học của một học kỳ"""
    return course_crud.get_courses_by_semester(db, semester_id, current_user.id)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy thông tin chi tiết một môn học"""
    course = course_crud.get_course(db, course_id, current_user.id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy môn học",
        )
    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cập nhật thông tin môn học"""
    course = course_crud.update_course(db, course_id, current_user.id, course_update)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy môn học",
        )
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Xóa môn học"""
    if not course_crud.delete_course(db, course_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy môn học",
        )
