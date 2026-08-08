"""Gửi email OTP qua Resend (fallback: in ra log khi chưa cấu hình API key)."""

from __future__ import annotations

import httpx

from app.core.config import settings


def mask_email(email: str) -> str:
    """user@gmail.com -> us***@gmail.com"""
    email = (email or "").strip()
    if "@" not in email:
        return "***"
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        masked_local = local[:1] + "***"
    else:
        masked_local = local[:2] + "***"
    return f"{masked_local}@{domain}"


def send_otp_email(to_email: str, otp: str) -> None:
    subject = "Mã OTP đặt lại mật khẩu - GPA Calculator"
    html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
      <h2>Đặt lại mật khẩu</h2>
      <p>Mã OTP của bạn là:</p>
      <p style="font-size: 28px; font-weight: bold; letter-spacing: 6px;">{otp}</p>
      <p>Mã có hiệu lực trong <strong>{settings.OTP_EXPIRE_MINUTES} phút</strong>.</p>
      <p>Nếu bạn không yêu cầu, hãy bỏ qua email này.</p>
    </div>
    """

    if not settings.RESEND_API_KEY:
        print(f"[DEV EMAIL] To={to_email} OTP={otp} (chưa cấu hình RESEND_API_KEY)")
        return

    response = httpx.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": settings.EMAIL_FROM,
            "to": [to_email],
            "subject": subject,
            "html": html,
        },
        timeout=20.0,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Gửi email thất bại: {response.status_code} {response.text}")
