from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.semester import get_semester
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.utils.gpa import convert_score_to_letter_and_gpa


def create_course(db: Session, course: CourseCreate, user_id: int) -> Optional[Course]:
    semester = get_semester(db, course.semester_id, user_id)
    if not semester:
        return None

    letter_grade, grade_point = convert_score_to_letter_and_gpa(course.score)

    db_course = Course(
        course_code=course.course_code,
        course_name=course.course_name,
        credits=course.credits,
        score=course.score,
        letter_grade=letter_grade,
        grade_point=grade_point,
        semester_id=course.semester_id,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_courses_by_semester(db: Session, semester_id: int, user_id: int) -> List[Course]:
    semester = get_semester(db, semester_id, user_id)
    if not semester:
        return []
    return db.query(Course).filter(Course.semester_id == semester_id).all()


def get_course(db: Session, course_id: int, user_id: int) -> Optional[Course]:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return None
    semester = get_semester(db, course.semester_id, user_id)
    if not semester:
        return None
    return course


def update_course(
    db: Session,
    course_id: int,
    user_id: int,
    course_update: CourseUpdate,
) -> Optional[Course]:
    db_course = get_course(db, course_id, user_id)
    if not db_course:
        return None

    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)

    if "score" in update_data:
        letter_grade, grade_point = convert_score_to_letter_and_gpa(db_course.score)
        db_course.letter_grade = letter_grade
        db_course.grade_point = grade_point

    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int, user_id: int) -> bool:
    db_course = get_course(db, course_id, user_id)
    if not db_course:
        return False
    db.delete(db_course)
    db.commit()
    return True
