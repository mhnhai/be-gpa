from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.major import Major
from app.schemas.major import MajorCreate, MajorUpdate


def create_major(db: Session, data: MajorCreate) -> Major:
    major = Major(**data.model_dump())
    db.add(major)
    db.commit()
    db.refresh(major)
    return major


def get_majors(
    db: Session,
    major_type: Optional[str] = None,
    cohort_id: Optional[int] = None,
    active_only: bool = True,
) -> List[Major]:
    query = db.query(Major)
    if active_only:
        query = query.filter(Major.is_active == True)  # noqa: E712
    if major_type:
        query = query.filter(Major.major_type == major_type)
    if cohort_id is not None:
        # Ngành riêng của khóa + (tuỳ chọn) không trả common ở đây
        query = query.filter(Major.cohort_id == cohort_id)
    return query.order_by(Major.major_type, Major.name).all()


def get_major(db: Session, major_id: int) -> Optional[Major]:
    return db.query(Major).filter(Major.id == major_id).first()


def get_major_by_name(db: Session, name: str) -> Optional[Major]:
    return db.query(Major).filter(Major.name == name).first()


def get_major_by_code(db: Session, code: str) -> Optional[Major]:
    return db.query(Major).filter(Major.code == code).first()


def update_major(db: Session, major_id: int, data: MajorUpdate) -> Optional[Major]:
    major = get_major(db, major_id)
    if not major:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(major, field, value)
    db.commit()
    db.refresh(major)
    return major


def delete_major(db: Session, major_id: int) -> bool:
    major = get_major(db, major_id)
    if not major:
        return False
    db.delete(major)
    db.commit()
    return True
