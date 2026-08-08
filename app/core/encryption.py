"""Mã hóa điểm số khi lưu DB (Fernet/AES).

Không dùng bcrypt cho điểm vì bcrypt là hash một chiều —
không giải mã được để tính GPA / hiển thị.
"""

from __future__ import annotations

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings


def _fernet() -> Fernet:
    # Derive 32-byte key từ SECRET_KEY (ổn định giữa các lần deploy nếu SECRET_KEY không đổi)
    digest = hashlib.sha256(settings.SECRET_KEY.encode("utf-8")).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def encrypt_text(plain: str) -> str:
    return _fernet().encrypt(plain.encode("utf-8")).decode("utf-8")


def decrypt_text(token: str) -> str:
    return _fernet().decrypt(token.encode("utf-8")).decode("utf-8")


def encrypt_float(value: float) -> str:
    return encrypt_text(repr(float(value)))


def decrypt_float(token: str) -> float:
    return float(decrypt_text(token))


def looks_encrypted(value: str) -> bool:
    """Fernet token thường bắt đầu bằng gAAAA."""
    return isinstance(value, str) and value.startswith("gAAAA")
