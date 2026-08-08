from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.core.security import get_password_hash
from app.models.cohort import Cohort
from app.models.major import Major
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdateProfile


def create_user(db: Session, user: UserCreate) -> User:
    if user.cohort_id and not db.query(Cohort).filter(Cohort.id == user.cohort_id).first():
        raise ValueError("cohort_id không hợp lệ")
    if user.major_id:
        major = db.query(Major).filter(Major.id == user.major_id).first()
        if not major:
            raise ValueError("major_id không hợp lệ")
        if major.major_type == "common":
            raise ValueError("User phải chọn ngành riêng (specific), không chọn ngành chung")

    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        cohort_id=user.cohort_id,
        major_id=user.major_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    return (
        db.query(User)
        .options(joinedload(User.cohort), joinedload(User.major))
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return (
        db.query(User)
        .options(joinedload(User.cohort), joinedload(User.major))
        .filter(User.username == username)
        .first()
    )


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def update_user_profile(
    db: Session, user: User, data: UserUpdateProfile
) -> User:
    payload = data.model_dump(exclude_unset=True)

    if "cohort_id" in payload and payload["cohort_id"] is not None:
        if not db.query(Cohort).filter(Cohort.id == payload["cohort_id"]).first():
            raise ValueError("cohort_id không hợp lệ")

    if "major_id" in payload and payload["major_id"] is not None:
        major = db.query(Major).filter(Major.id == payload["major_id"]).first()
        if not major:
            raise ValueError("major_id không hợp lệ")
        if major.major_type == "common":
            raise ValueError("User phải chọn ngành riêng (specific), không chọn ngành chung")

    for field, value in payload.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return get_user(db, user.id) or user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    from app.core.security import verify_password

    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
