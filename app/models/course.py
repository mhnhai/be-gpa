from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.types import EncryptedFloat


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, nullable=False)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    # Điểm được mã hóa khi lưu DB (Fernet), app vẫn dùng float
    score = Column(EncryptedFloat, nullable=False)
    letter_grade = Column(String)
    grade_point = Column(EncryptedFloat)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    semester = relationship("Semester", back_populates="courses")
