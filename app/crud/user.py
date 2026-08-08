from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.core.security import get_password_hash, verify_password
from app.models.cohort import Cohort
from app.models.major import Major
from app.models.user import User
from app.schemas.user import ChangePasswordRequest, UserCreate, UserUpdateProfile


def create_user(db: Session, user: UserCreate) -> User:
    if user.cohort_id and not db.query(Cohort).filter(Cohort.id == user.cohort_id).first():
        raise ValueError("cohort_id không hợp lệ")
    if user.major_id:
        major = db.query(Major).filter(Major.id == user.major_id).first()
        if not major:
            raise ValueError("major_id không hợp lệ")
        if major.major_type == "common":
            raise ValueError("User phải chọn ngành riêng (specific), không chọn ngành chung")
        if user.cohort_id and major.cohort_id and major.cohort_id != user.cohort_id:
            raise ValueError("Ngành học không thuộc khóa học đã chọn")
        if major.cohort_id and not user.cohort_id:
            raise ValueError("Phải chọn khóa học tương ứng với ngành")

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
    """Chỉ cập nhật email và full_name."""
    payload = data.model_dump(exclude_unset=True)

    if "email" in payload and payload["email"] is not None:
        new_email = str(payload["email"]).strip()
        existing = (
            db.query(User)
            .filter(User.email.ilike(new_email), User.id != user.id)
            .first()
        )
        if existing:
            raise ValueError("Email đã được sử dụng bởi tài khoản khác")
        user.email = new_email

    if "full_name" in payload:
        user.full_name = payload["full_name"]

    db.commit()
    db.refresh(user)
    return get_user(db, user.id) or user


def change_password(
    db: Session, user: User, data: ChangePasswordRequest
) -> None:
    if data.new_password != data.confirm_password:
        raise ValueError("Mật khẩu xác nhận không khớp")
    if not verify_password(data.old_password, user.hashed_password):
        raise ValueError("Mật khẩu cũ không đúng")
    if verify_password(data.new_password, user.hashed_password):
        raise ValueError("Mật khẩu mới phải khác mật khẩu cũ")

    user.hashed_password = get_password_hash(data.new_password)
    db.commit()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
