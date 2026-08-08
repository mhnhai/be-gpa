from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.crud import semester as semester_crud
from app.crud import gpa as gpa_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.semester import (
    SemesterCreate,
    SemesterResponse,
    SemesterUpdate,
    SemesterWithGPA,
)

router = APIRouter(prefix="/api/semesters", tags=["Semesters"])


@router.post("/", response_model=SemesterResponse, status_code=status.HTTP_201_CREATED)
def create_semester(
    semester: SemesterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Tạo học kỳ mới"""
    return semester_crud.create_semester(db, semester, current_user.id)


@router.get("/", response_model=List[SemesterResponse])
def get_semesters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy danh sách tất cả học kỳ của người dùng"""
    return semester_crud.get_semesters(db, current_user.id)


@router.get("/{semester_id}", response_model=SemesterWithGPA)
def get_semester(
    semester_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy thông tin chi tiết học kỳ kèm GPA"""
    semester = gpa_crud.get_semester_gpa(db, semester_id, current_user.id)
    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học kỳ",
        )
    return semester


@router.put("/{semester_id}", response_model=SemesterResponse)
def update_semester(
    semester_id: int,
    semester_update: SemesterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cập nhật thông tin học kỳ"""
    semester = semester_crud.update_semester(
        db, semester_id, current_user.id, semester_update
    )
    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học kỳ",
        )
    return semester


@router.delete("/{semester_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_semester(
    semester_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Xóa học kỳ"""
    if not semester_crud.delete_semester(db, semester_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học kỳ",
        )
