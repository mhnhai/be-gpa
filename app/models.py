from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class CourseCatalog(Base):
    """Kho môn học có sẵn"""
    __tablename__ = "course_catalog"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True, nullable=False)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    semesters = relationship("Semester", back_populates="user", cascade="all, delete-orphan")


class Semester(Base):
    __tablename__ = "semesters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g., "Học kỳ 1 - Năm 2024"
    year = Column(Integer, nullable=False)
    semester_number = Column(Integer, nullable=False)  # 1, 2, or 3 (hè)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="semesters")
    courses = relationship("Course", back_populates="semester", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, nullable=False)  # Mã học phần
    course_name = Column(String, nullable=False)  # Tên học phần
    credits = Column(Integer, nullable=False)  # Số tín chỉ
    score = Column(Float, nullable=False)  # Điểm số (thang 10)
    letter_grade = Column(String)  # Điểm chữ (A, B+, B, etc.)
    grade_point = Column(Float)  # Điểm hệ 4
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    semester = relationship("Semester", back_populates="courses")

