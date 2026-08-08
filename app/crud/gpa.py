from typing import Optional

from sqlalchemy.orm import Session

from app.crud.semester import get_semester, get_semesters
from app.schemas.course import CourseResponse
from app.schemas.gpa import GPASummary
from app.schemas.semester import SemesterWithGPA
from app.utils.gpa import calculate_gpa


def get_semester_gpa(
    db: Session,
    semester_id: int,
    user_id: int,
) -> Optional[SemesterWithGPA]:
    semester = get_semester(db, semester_id, user_id)
    if not semester:
        return None

    gpa, total_credits = calculate_gpa(semester.courses)

    return SemesterWithGPA(
        id=semester.id,
        name=semester.name,
        year=semester.year,
        semester_number=semester.semester_number,
        user_id=semester.user_id,
        created_at=semester.created_at,
        courses=[CourseResponse.model_validate(c) for c in semester.courses],
        semester_gpa=gpa,
        total_credits=total_credits,
    )


def get_gpa_summary(db: Session, user_id: int) -> GPASummary:
    semesters = get_semesters(db, user_id)

    all_courses = []
    semesters_with_gpa = []

    for semester in semesters:
        gpa, total_credits = calculate_gpa(semester.courses)
        all_courses.extend(semester.courses)

        semesters_with_gpa.append(
            SemesterWithGPA(
                id=semester.id,
                name=semester.name,
                year=semester.year,
                semester_number=semester.semester_number,
                user_id=semester.user_id,
                created_at=semester.created_at,
                courses=[CourseResponse.model_validate(c) for c in semester.courses],
                semester_gpa=gpa,
                total_credits=total_credits,
            )
        )

    cumulative_gpa, total_credits = calculate_gpa(all_courses)

    return GPASummary(
        cumulative_gpa=cumulative_gpa,
        total_credits=total_credits,
        total_courses=len(all_courses),
        semesters=semesters_with_gpa,
    )
