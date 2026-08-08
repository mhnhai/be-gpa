from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.crud import major as major_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.major import MajorCreate, MajorResponse, MajorUpdate

router = APIRouter(prefix="/api/majors", tags=["Majors"])


@router.get("/", response_model=List[MajorResponse])
def list_majors(
    major_type: Optional[str] = Query(
        None, description="Lọc theo loại: common | specific"
    ),
    db: Session = Depends(get_db),
):
    """Danh sách ngành học (chung / riêng)"""
    if major_type and major_type not in ("common", "specific"):
        raise HTTPException(
            status_code=400,
            detail="major_type phải là 'common' hoặc 'specific'",
        )
    return major_crud.get_majors(db, major_type=major_type)


@router.post("/", response_model=MajorResponse, status_code=status.HTTP_201_CREATED)
def create_major(
    data: MajorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if major_crud.get_major_by_name(db, data.name):
        raise HTTPException(status_code=400, detail="Tên ngành đã tồn tại")
    return major_crud.create_major(db, data)


@router.get("/{major_id}", response_model=MajorResponse)
def get_major(major_id: int, db: Session = Depends(get_db)):
    major = major_crud.get_major(db, major_id)
    if not major:
        raise HTTPException(status_code=404, detail="Không tìm thấy ngành học")
    return major


@router.put("/{major_id}", response_model=MajorResponse)
def update_major(
    major_id: int,
    data: MajorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    major = major_crud.update_major(db, major_id, data)
    if not major:
        raise HTTPException(status_code=404, detail="Không tìm thấy ngành học")
    return major


@router.delete("/{major_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_major(
    major_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not major_crud.delete_major(db, major_id):
        raise HTTPException(status_code=404, detail="Không tìm thấy ngành học")
