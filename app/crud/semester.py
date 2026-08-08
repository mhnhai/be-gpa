from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.semester import Semester
from app.schemas.semester import SemesterCreate, SemesterUpdate


def create_semester(db: Session, semester: SemesterCreate, user_id: int) -> Semester:
    db_semester = Semester(
        name=semester.name,
        year=semester.year,
        semester_number=semester.semester_number,
        user_id=user_id,
    )
    db.add(db_semester)
    db.commit()
    db.refresh(db_semester)
    return db_semester


def get_semesters(db: Session, user_id: int) -> List[Semester]:
    return (
        db.query(Semester)
        .filter(Semester.user_id == user_id)
        .order_by(Semester.year.desc(), Semester.semester_number.desc())
        .all()
    )


def get_semester(db: Session, semester_id: int, user_id: int) -> Optional[Semester]:
    return (
        db.query(Semester)
        .filter(Semester.id == semester_id, Semester.user_id == user_id)
        .first()
    )


def update_semester(
    db: Session,
    semester_id: int,
    user_id: int,
    semester_update: SemesterUpdate,
) -> Optional[Semester]:
    db_semester = get_semester(db, semester_id, user_id)
    if not db_semester:
        return None

    update_data = semester_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_semester, field, value)

    db.commit()
    db.refresh(db_semester)
    return db_semester


def delete_semester(db: Session, semester_id: int, user_id: int) -> bool:
    db_semester = get_semester(db, semester_id, user_id)
    if not db_semester:
        return False
    db.delete(db_semester)
    db.commit()
    return True
