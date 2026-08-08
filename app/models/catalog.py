from sqlalchemy import Column, Integer, String, Boolean

from app.db.base import Base


class CourseCatalog(Base):
    """Kho môn học có sẵn"""

    __tablename__ = "course_catalog"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True, nullable=False)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
