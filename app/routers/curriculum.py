from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.deps import get_current_user
from app.crud import curriculum as curriculum_crud
from app.db.session import get_db
from app.models.curriculum import CurriculumItem
from app.models.user import User
from app.schemas.curriculum import (
    CurriculumBulkCreate,
    CurriculumItemCreate,
    CurriculumItemResponse,
    UserCurriculumResponse,
)

router = APIRouter(prefix="/api/curriculum", tags=["Curriculum"])


def _get_item(db: Session, item_id: int) -> CurriculumItem | None:
    return (
        db.query(CurriculumItem)
        .options(joinedload(CurriculumItem.course), joinedload(CurriculumItem.major))
        .filter(CurriculumItem.id == item_id)
        .first()
    )


@router.get("/me", response_model=UserCurriculumResponse)
def get_my_curriculum(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lấy CTĐT của user hiện tại =
    môn học chung (common) + môn học ngành riêng của user.
    """
    return curriculum_crud.get_user_curriculum(db, current_user)


@router.get("/major/{major_id}", response_model=List[CurriculumItemResponse])
def get_curriculum_by_major(major_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách môn CTĐT theo ngành"""
    return curriculum_crud.get_curriculum_by_major(db, major_id)


@router.post("/", response_model=CurriculumItemResponse, status_code=status.HTTP_201_CREATED)
def add_curriculum_item(
    data: CurriculumItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = curriculum_crud.add_curriculum_item(db, data)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy ngành hoặc môn học trong kho",
        )
    loaded = _get_item(db, item.id)
    return loaded or item


@router.post(
    "/bulk",
    response_model=List[CurriculumItemResponse],
    status_code=status.HTTP_201_CREATED,
)
def bulk_add_curriculum(
    data: CurriculumBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = curriculum_crud.bulk_add_curriculum_items(db, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy ngành học")
    return curriculum_crud.get_curriculum_by_major(db, data.major_id)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_curriculum_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not curriculum_crud.delete_curriculum_item(db, item_id):
        raise HTTPException(status_code=404, detail="Không tìm thấy mục CTĐT")
