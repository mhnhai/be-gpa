"""SQLAlchemy types: mã hóa float khi ghi / giải mã khi đọc."""

from __future__ import annotations

from sqlalchemy import String, TypeDecorator

from app.core.encryption import (
    decrypt_float,
    encrypt_float,
    looks_encrypted,
)


class EncryptedFloat(TypeDecorator):
    """
    Lưu điểm dưới dạng chuỗi đã mã hóa (Fernet).
    App vẫn thấy/ghi kiểu float bình thường.
    Tương thích dữ liệu cũ dạng số plaintext sau khi ALTER sang TEXT.
    """

    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return encrypt_float(float(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).strip()
        if not text:
            return None
        if looks_encrypted(text):
            try:
                return decrypt_float(text)
            except Exception:
                raise ValueError("Không giải mã được điểm — kiểm tra SECRET_KEY")
        # Legacy plaintext sau migration ::text
        return float(text)
