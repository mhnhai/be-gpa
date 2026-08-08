from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.crud import cohort as cohort_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.cohort import CohortCreate, CohortResponse, CohortUpdate

router = APIRouter(prefix="/api/cohorts", tags=["Cohorts"])


@router.get("/", response_model=List[CohortResponse])
def list_cohorts(db: Session = Depends(get_db)):
    """Danh sách khóa học (K50, K51, ...)"""
    return cohort_crud.get_cohorts(db)


@router.post("/", response_model=CohortResponse, status_code=status.HTTP_201_CREATED)
def create_cohort(
    data: CohortCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Thêm khóa học mới"""
    if cohort_crud.get_cohort_by_code(db, data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Khóa học {data.code} đã tồn tại",
        )
    return cohort_crud.create_cohort(db, data)


@router.put("/{cohort_id}", response_model=CohortResponse)
def update_cohort(
    cohort_id: int,
    data: CohortUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cohort = cohort_crud.update_cohort(db, cohort_id, data)
    if not cohort:
        raise HTTPException(status_code=404, detail="Không tìm thấy khóa học")
    return cohort


@router.delete("/{cohort_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cohort(
    cohort_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not cohort_crud.delete_cohort(db, cohort_id):
        raise HTTPException(status_code=404, detail="Không tìm thấy khóa học")
