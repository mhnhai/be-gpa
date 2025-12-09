from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import CourseCatalogResponse, BulkAddCourses, CourseResponse
from ..auth import get_current_user
from ..models import User, CourseCatalog, Course, Semester
from ..utils import convert_score_to_letter_and_gpa

router = APIRouter(prefix="/api/catalog", tags=["Course Catalog"])


@router.get("/", response_model=List[CourseCatalogResponse])
def get_catalog(
    search: Optional[str] = Query(None, description="Tìm kiếm theo mã hoặc tên môn học"),
    db: Session = Depends(get_db)
):
    """Lấy danh sách môn học trong kho"""
    query = db.query(CourseCatalog).filter(CourseCatalog.is_active == True)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (CourseCatalog.course_code.ilike(search_term)) |
            (CourseCatalog.course_name.ilike(search_term))
        )
    
    return query.order_by(CourseCatalog.course_code).all()


@router.post("/bulk-add", response_model=List[CourseResponse])
def bulk_add_courses(
    data: BulkAddCourses,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Thêm nhiều môn học từ kho vào học kỳ"""
    # Verify semester belongs to user
    semester = db.query(Semester).filter(
        Semester.id == data.semester_id,
        Semester.user_id == current_user.id
    ).first()
    
    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học kỳ"
        )
    
    # Get catalog courses
    catalog_courses = db.query(CourseCatalog).filter(
        CourseCatalog.id.in_(data.course_ids),
        CourseCatalog.is_active == True
    ).all()
    
    if not catalog_courses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không tìm thấy môn học nào trong kho"
        )
    
    # Check for existing courses in semester
    existing_codes = {c.course_code for c in semester.courses}
    
    added_courses = []
    for catalog_course in catalog_courses:
        if catalog_course.course_code in existing_codes:
            continue  # Skip if already exists
        
        letter_grade, grade_point = convert_score_to_letter_and_gpa(data.default_score)
        
        new_course = Course(
            course_code=catalog_course.course_code,
            course_name=catalog_course.course_name,
            credits=catalog_course.credits,
            score=data.default_score,
            letter_grade=letter_grade,
            grade_point=grade_point,
            semester_id=data.semester_id
        )
        db.add(new_course)
        added_courses.append(new_course)
    
    db.commit()
    
    for course in added_courses:
        db.refresh(course)
    
    return added_courses


@router.get("/count")
def get_catalog_count(db: Session = Depends(get_db)):
    """Đếm số môn học trong kho"""
    count = db.query(CourseCatalog).filter(CourseCatalog.is_active == True).count()
    return {"count": count}

