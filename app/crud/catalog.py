from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.catalog import CourseCatalog
from app.models.course import Course
from app.models.semester import Semester
from app.schemas.catalog import BulkAddCourses
from app.utils.gpa import convert_score_to_letter_and_gpa


def get_catalog(db: Session, search: Optional[str] = None) -> List[CourseCatalog]:
    query = db.query(CourseCatalog).filter(CourseCatalog.is_active == True)  # noqa: E712

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (CourseCatalog.course_code.ilike(search_term))
            | (CourseCatalog.course_name.ilike(search_term))
        )

    return query.order_by(CourseCatalog.course_code).all()


def get_catalog_count(db: Session) -> int:
    return db.query(CourseCatalog).filter(CourseCatalog.is_active == True).count()  # noqa: E712


def bulk_add_courses(
    db: Session,
    data: BulkAddCourses,
    user_id: int,
) -> Optional[List[Course]]:
    semester = (
        db.query(Semester)
        .filter(Semester.id == data.semester_id, Semester.user_id == user_id)
        .first()
    )
    if not semester:
        return None

    catalog_courses = (
        db.query(CourseCatalog)
        .filter(
            CourseCatalog.id.in_(data.course_ids),
            CourseCatalog.is_active == True,  # noqa: E712
        )
        .all()
    )
    if not catalog_courses:
        return []

    existing_codes = {c.course_code for c in semester.courses}
    added_courses: List[Course] = []

    for catalog_course in catalog_courses:
        if catalog_course.course_code in existing_codes:
            continue

        letter_grade, grade_point = convert_score_to_letter_and_gpa(data.default_score)
        new_course = Course(
            course_code=catalog_course.course_code,
            course_name=catalog_course.course_name,
            credits=catalog_course.credits,
            score=data.default_score,
            letter_grade=letter_grade,
            grade_point=grade_point,
            semester_id=data.semester_id,
        )
        db.add(new_course)
        added_courses.append(new_course)

    db.commit()
    for course in added_courses:
        db.refresh(course)

    return added_courses
