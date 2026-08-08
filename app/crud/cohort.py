from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.cohort import Cohort
from app.schemas.cohort import CohortCreate, CohortUpdate


def create_cohort(db: Session, data: CohortCreate) -> Cohort:
    cohort = Cohort(**data.model_dump())
    db.add(cohort)
    db.commit()
    db.refresh(cohort)
    return cohort


def get_cohorts(db: Session, active_only: bool = True) -> List[Cohort]:
    query = db.query(Cohort)
    if active_only:
        query = query.filter(Cohort.is_active == True)  # noqa: E712
    return query.order_by(Cohort.code).all()


def get_cohort(db: Session, cohort_id: int) -> Optional[Cohort]:
    return db.query(Cohort).filter(Cohort.id == cohort_id).first()


def get_cohort_by_code(db: Session, code: str) -> Optional[Cohort]:
    return db.query(Cohort).filter(Cohort.code == code).first()


def update_cohort(
    db: Session, cohort_id: int, data: CohortUpdate
) -> Optional[Cohort]:
    cohort = get_cohort(db, cohort_id)
    if not cohort:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cohort, field, value)
    db.commit()
    db.refresh(cohort)
    return cohort


def delete_cohort(db: Session, cohort_id: int) -> bool:
    cohort = get_cohort(db, cohort_id)
    if not cohort:
        return False
    db.delete(cohort)
    db.commit()
    return True
