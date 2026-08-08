from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class CurriculumItem(Base):
    """
    CTĐT: môn học thuộc một ngành (chung hoặc riêng).
    Một ngành có nhiều môn từ course_catalog.
    """

    __tablename__ = "curriculum_items"
    __table_args__ = (
        UniqueConstraint("major_id", "course_catalog_id", name="uq_major_course"),
    )

    id = Column(Integer, primary_key=True, index=True)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=False, index=True)
    course_catalog_id = Column(
        Integer, ForeignKey("course_catalog.id"), nullable=False, index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    major = relationship("Major", back_populates="curriculum_items")
    course = relationship("CourseCatalog")
