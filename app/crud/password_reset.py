from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_password_reset_token,
    decode_password_reset_token,
    get_password_hash,
    verify_password,
)
from app.models.password_reset import PasswordResetOTP
from app.models.user import User
from app.services.email import mask_email, send_otp_email


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def request_password_reset(db: Session, email: str) -> dict:
    """
    Luôn trả masked_email để FE hiển thị.
    Chỉ gửi OTP nếu email tồn tại.
    """
    normalized = email.strip().lower()
    masked = mask_email(normalized)
    user = db.query(User).filter(User.email == normalized).first()
    # fallback: email có thể lưu mixed-case
    if not user:
        user = db.query(User).filter(User.email.ilike(normalized)).first()

    if not user:
        return {
            "message": f"Nếu email tồn tại, mã OTP đã được gửi tới {masked}",
            "masked_email": masked,
            "expires_in_minutes": settings.OTP_EXPIRE_MINUTES,
        }

    # Chống spam: cooldown gửi lại
    latest = (
        db.query(PasswordResetOTP)
        .filter(PasswordResetOTP.user_id == user.id)
        .order_by(PasswordResetOTP.created_at.desc())
        .first()
    )
    if latest and latest.created_at:
        created = latest.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        elapsed = (_utcnow() - created).total_seconds()
        if elapsed < settings.OTP_RESEND_COOLDOWN_SECONDS:
            wait = int(settings.OTP_RESEND_COOLDOWN_SECONDS - elapsed)
            raise ValueError(f"Vui lòng đợi {wait}s trước khi gửi lại OTP")

    # Invalidate OTP cũ chưa dùng
    db.query(PasswordResetOTP).filter(
        PasswordResetOTP.user_id == user.id,
        PasswordResetOTP.is_used == False,  # noqa: E712
    ).update({"is_used": True})

    otp = _generate_otp()
    record = PasswordResetOTP(
        user_id=user.id,
        email=user.email,
        otp_hash=get_password_hash(otp),
        expires_at=_utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
        attempts=0,
        is_used=False,
    )
    db.add(record)
    db.commit()

    send_otp_email(user.email, otp)

    return {
        "message": f"Đã gửi mã OTP tới email {mask_email(user.email)}",
        "masked_email": mask_email(user.email),
        "expires_in_minutes": settings.OTP_EXPIRE_MINUTES,
    }


def verify_otp(db: Session, email: str, otp: str) -> dict:
    normalized = email.strip().lower()
    user = db.query(User).filter(User.email.ilike(normalized)).first()
    if not user:
        raise ValueError("Email hoặc mã OTP không đúng")

    record = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.user_id == user.id,
            PasswordResetOTP.is_used == False,  # noqa: E712
        )
        .order_by(PasswordResetOTP.created_at.desc())
        .first()
    )
    if not record:
        raise ValueError("Không có mã OTP hợp lệ. Hãy yêu cầu gửi lại.")

    expires = record.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < _utcnow():
        record.is_used = True
        db.commit()
        raise ValueError("Mã OTP đã hết hạn")

    if record.attempts >= settings.OTP_MAX_ATTEMPTS:
        record.is_used = True
        db.commit()
        raise ValueError("Đã nhập sai quá số lần cho phép. Hãy gửi lại OTP.")

    if not verify_password(otp.strip(), record.otp_hash):
        record.attempts += 1
        db.commit()
        remaining = settings.OTP_MAX_ATTEMPTS - record.attempts
        raise ValueError(f"Mã OTP không đúng. Còn {max(remaining, 0)} lần thử.")

    record.is_used = True
    db.commit()

    reset_token = create_password_reset_token(user.id, user.email)
    return {
        "message": "Xác thực OTP thành công",
        "reset_token": reset_token,
        "expires_in_minutes": settings.RESET_TOKEN_EXPIRE_MINUTES,
    }


def reset_password(db: Session, reset_token: str, new_password: str) -> dict:
    payload = decode_password_reset_token(reset_token)
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Người dùng không tồn tại")

    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return {"message": "Đặt lại mật khẩu thành công. Vui lòng đăng nhập."}
