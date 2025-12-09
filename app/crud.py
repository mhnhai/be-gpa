from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas
from .auth import get_password_hash
from .utils import convert_score_to_letter_and_gpa, calculate_gpa


# ============ User CRUD ============
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


# ============ Semester CRUD ============
def create_semester(
    db: Session, 
    semester: schemas.SemesterCreate, 
    user_id: int
) -> models.Semester:
    db_semester = models.Semester(
        name=semester.name,
        year=semester.year,
        semester_number=semester.semester_number,
        user_id=user_id
    )
    db.add(db_semester)
    db.commit()
    db.refresh(db_semester)
    return db_semester


def get_semesters(db: Session, user_id: int) -> List[models.Semester]:
    return db.query(models.Semester)\
        .filter(models.Semester.user_id == user_id)\
        .order_by(models.Semester.year.desc(), models.Semester.semester_number.desc())\
        .all()


def get_semester(db: Session, semester_id: int, user_id: int) -> Optional[models.Semester]:
    return db.query(models.Semester)\
        .filter(models.Semester.id == semester_id, models.Semester.user_id == user_id)\
        .first()


def update_semester(
    db: Session, 
    semester_id: int, 
    user_id: int, 
    semester_update: schemas.SemesterUpdate
) -> Optional[models.Semester]:
    db_semester = get_semester(db, semester_id, user_id)
    if not db_semester:
        return None
    
    update_data = semester_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_semester, field, value)
    
    db.commit()
    db.refresh(db_semester)
    return db_semester


def delete_semester(db: Session, semester_id: int, user_id: int) -> bool:
    db_semester = get_semester(db, semester_id, user_id)
    if not db_semester:
        return False
    db.delete(db_semester)
    db.commit()
    return True


# ============ Course CRUD ============
def create_course(
    db: Session, 
    course: schemas.CourseCreate, 
    user_id: int
) -> Optional[models.Course]:
    # Verify semester belongs to user
    semester = get_semester(db, course.semester_id, user_id)
    if not semester:
        return None
    
    letter_grade, grade_point = convert_score_to_letter_and_gpa(course.score)
    
    db_course = models.Course(
        course_code=course.course_code,
        course_name=course.course_name,
        credits=course.credits,
        score=course.score,
        letter_grade=letter_grade,
        grade_point=grade_point,
        semester_id=course.semester_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_courses_by_semester(db: Session, semester_id: int, user_id: int) -> List[models.Course]:
    semester = get_semester(db, semester_id, user_id)
    if not semester:
        return []
    return db.query(models.Course)\
        .filter(models.Course.semester_id == semester_id)\
        .all()


def get_course(db: Session, course_id: int, user_id: int) -> Optional[models.Course]:
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        return None
    # Verify course belongs to user through semester
    semester = get_semester(db, course.semester_id, user_id)
    if not semester:
        return None
    return course


def update_course(
    db: Session, 
    course_id: int, 
    user_id: int, 
    course_update: schemas.CourseUpdate
) -> Optional[models.Course]:
    db_course = get_course(db, course_id, user_id)
    if not db_course:
        return None
    
    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    # Recalculate letter grade and grade point if score changed
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


# ============ GPA Calculation ============
def get_semester_gpa(db: Session, semester_id: int, user_id: int) -> Optional[schemas.SemesterWithGPA]:
    semester = get_semester(db, semester_id, user_id)
    if not semester:
        return None
    
    gpa, total_credits = calculate_gpa(semester.courses)
    
    return schemas.SemesterWithGPA(
        id=semester.id,
        name=semester.name,
        year=semester.year,
        semester_number=semester.semester_number,
        user_id=semester.user_id,
        created_at=semester.created_at,
        courses=[schemas.CourseResponse.model_validate(c) for c in semester.courses],
        semester_gpa=gpa,
        total_credits=total_credits
    )


def get_gpa_summary(db: Session, user_id: int) -> schemas.GPASummary:
    semesters = get_semesters(db, user_id)
    
    all_courses = []
    semesters_with_gpa = []
    
    for semester in semesters:
        gpa, total_credits = calculate_gpa(semester.courses)
        all_courses.extend(semester.courses)
        
        semesters_with_gpa.append(schemas.SemesterWithGPA(
            id=semester.id,
            name=semester.name,
            year=semester.year,
            semester_number=semester.semester_number,
            user_id=semester.user_id,
            created_at=semester.created_at,
            courses=[schemas.CourseResponse.model_validate(c) for c in semester.courses],
            semester_gpa=gpa,
            total_credits=total_credits
        ))
    
    cumulative_gpa, total_credits = calculate_gpa(all_courses)
    
    return schemas.GPASummary(
        cumulative_gpa=cumulative_gpa,
        total_credits=total_credits,
        total_courses=len(all_courses),
        semesters=semesters_with_gpa
    )

