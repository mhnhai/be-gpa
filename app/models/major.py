from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Major(Base):
    """
    Ngành học gắn với một khóa (cohort).
    - major_type = "common": môn chung, cohort_id = NULL (áp dụng mọi khóa)
    - major_type = "specific": ngành riêng, bắt buộc có cohort_id
      ví dụ: Luật tư pháp chỉ thuộc K50, Hóa học chỉ thuộc K51
    """

    __tablename__ = "majors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=True, index=True)
    major_type = Column(String, nullable=False, default="specific")  # common | specific
    description = Column(String, nullable=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"), nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cohort = relationship("Cohort", back_populates="majors")
    curriculum_items = relationship(
        "CurriculumItem",
        back_populates="major",
        cascade="all, delete-orphan",
    )
    users = relationship("User", back_populates="major")
