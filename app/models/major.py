from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Major(Base):
    """
    Ngành học.
    - major_type = "common": ngành/khối môn học chung (Triết, Lịch sử Đảng, ...)
    - major_type = "specific": ngành riêng (Luật, Hóa học, ...)
    """

    __tablename__ = "majors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=True, index=True)
    major_type = Column(String, nullable=False, default="specific")  # common | specific
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    curriculum_items = relationship(
        "CurriculumItem",
        back_populates="major",
        cascade="all, delete-orphan",
    )
    users = relationship("User", back_populates="major")
