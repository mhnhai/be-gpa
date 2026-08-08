from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Semester(Base):
    __tablename__ = "semesters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    semester_number = Column(Integer, nullable=False)  # 1, 2, or 3 (hè)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="semesters")
    courses = relationship(
        "Course",
        back_populates="semester",
        cascade="all, delete-orphan",
    )
