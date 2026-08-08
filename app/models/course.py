from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, nullable=False)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    letter_grade = Column(String)
    grade_point = Column(Float)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    semester = relationship("Semester", back_populates="courses")
