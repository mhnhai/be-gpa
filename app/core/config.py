import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/gpa_db",
    )
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production-abc123xyz789",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5173",
    )

    class Config:
        env_file = ".env"


settings = Settings()
