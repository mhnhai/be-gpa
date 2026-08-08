from typing import List, Optional, Set

from sqlalchemy.orm import Session, joinedload

from app.models.catalog import CourseCatalog
from app.models.curriculum import CurriculumItem
from app.models.major import Major
from app.models.user import User
from app.schemas.catalog import CourseCatalogResponse
from app.schemas.curriculum import (
    CurriculumBulkCreate,
    CurriculumItemCreate,
    UserCurriculumResponse,
)
from app.schemas.major import MajorResponse


def add_curriculum_item(
    db: Session, data: CurriculumItemCreate
) -> Optional[CurriculumItem]:
    major = db.query(Major).filter(Major.id == data.major_id).first()
    course = (
        db.query(CourseCatalog)
        .filter(CourseCatalog.id == data.course_catalog_id)
        .first()
    )
    if not major or not course:
        return None

    existing = (
        db.query(CurriculumItem)
        .filter(
            CurriculumItem.major_id == data.major_id,
            CurriculumItem.course_catalog_id == data.course_catalog_id,
        )
        .first()
    )
    if existing:
        return existing

    item = CurriculumItem(
        major_id=data.major_id,
        course_catalog_id=data.course_catalog_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def bulk_add_curriculum_items(
    db: Session, data: CurriculumBulkCreate
) -> Optional[List[CurriculumItem]]:
    major = db.query(Major).filter(Major.id == data.major_id).first()
    if not major:
        return None

    existing_ids: Set[int] = {
        item.course_catalog_id
        for item in db.query(CurriculumItem)
        .filter(CurriculumItem.major_id == data.major_id)
        .all()
    }

    catalog_courses = (
        db.query(CourseCatalog)
        .filter(
            CourseCatalog.id.in_(data.course_catalog_ids),
            CourseCatalog.is_active == True,  # noqa: E712
        )
        .all()
    )

    added: List[CurriculumItem] = []
    for course in catalog_courses:
        if course.id in existing_ids:
            continue
        item = CurriculumItem(major_id=data.major_id, course_catalog_id=course.id)
        db.add(item)
        added.append(item)

    db.commit()
    for item in added:
        db.refresh(item)
    return added


def get_curriculum_by_major(
    db: Session, major_id: int
) -> List[CurriculumItem]:
    return (
        db.query(CurriculumItem)
        .options(joinedload(CurriculumItem.course), joinedload(CurriculumItem.major))
        .filter(CurriculumItem.major_id == major_id)
        .all()
    )


def delete_curriculum_item(db: Session, item_id: int) -> bool:
    item = db.query(CurriculumItem).filter(CurriculumItem.id == item_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def _courses_for_majors(db: Session, major_ids: List[int]) -> List[CourseCatalog]:
    if not major_ids:
        return []
    items = (
        db.query(CurriculumItem)
        .options(joinedload(CurriculumItem.course))
        .filter(CurriculumItem.major_id.in_(major_ids))
        .all()
    )
    courses = []
    seen = set()
    for item in items:
        if item.course and item.course.id not in seen:
            seen.add(item.course.id)
            courses.append(item.course)
    return sorted(courses, key=lambda c: c.course_code)


def get_user_curriculum(db: Session, user: User) -> UserCurriculumResponse:
    common_majors = (
        db.query(Major)
        .filter(Major.major_type == "common", Major.is_active == True)  # noqa: E712
        .all()
    )
    common_ids = [m.id for m in common_majors]
    common_courses = _courses_for_majors(db, common_ids)

    major = None
    major_courses: List[CourseCatalog] = []
    if user.major_id:
        major = db.query(Major).filter(Major.id == user.major_id).first()
        if major:
            major_courses = _courses_for_majors(db, [major.id])

    seen = set()
    all_courses: List[CourseCatalog] = []
    for course in common_courses + major_courses:
        if course.id not in seen:
            seen.add(course.id)
            all_courses.append(course)

    return UserCurriculumResponse(
        major=MajorResponse.model_validate(major) if major else None,
        common_courses=[CourseCatalogResponse.model_validate(c) for c in common_courses],
        major_courses=[CourseCatalogResponse.model_validate(c) for c in major_courses],
        all_courses=[CourseCatalogResponse.model_validate(c) for c in all_courses],
    )
