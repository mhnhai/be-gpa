from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.crud import catalog as catalog_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.catalog import BulkAddCourses, CourseCatalogResponse
from app.schemas.course import CourseResponse

router = APIRouter(prefix="/api/catalog", tags=["Course Catalog"])


@router.get("/", response_model=List[CourseCatalogResponse])
def get_catalog(
    search: Optional[str] = Query(None, description="Tìm kiếm theo mã hoặc tên môn học"),
    db: Session = Depends(get_db),
):
    """Lấy danh sách môn học trong kho"""
    return catalog_crud.get_catalog(db, search)


@router.post("/bulk-add", response_model=List[CourseResponse])
def bulk_add_courses(
    data: BulkAddCourses,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Thêm nhiều môn học từ kho vào học kỳ"""
    result = catalog_crud.bulk_add_courses(db, data, current_user.id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học kỳ",
        )

    # Empty list with requested IDs may mean none found in catalog
    if result == [] and data.course_ids:
        from app.models.catalog import CourseCatalog

        found = (
            db.query(CourseCatalog)
            .filter(
                CourseCatalog.id.in_(data.course_ids),
                CourseCatalog.is_active == True,  # noqa: E712
            )
            .count()
        )
        if found == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không tìm thấy môn học nào trong kho",
            )

    return result


@router.get("/count")
def get_catalog_count(db: Session = Depends(get_db)):
    """Đếm số môn học trong kho"""
    return {"count": catalog_crud.get_catalog_count(db)}
