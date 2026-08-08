from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.crud import gpa as gpa_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.gpa import GPASummary

router = APIRouter(prefix="/api/gpa", tags=["GPA"])


@router.get("/summary", response_model=GPASummary)
def get_gpa_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lấy tổng hợp GPA bao gồm:
    - Điểm trung bình chung tích lũy (Cumulative GPA)
    - Tổng số tín chỉ đã học
    - Tổng số môn học
    - Danh sách học kỳ với GPA từng kỳ
    """
    return gpa_crud.get_gpa_summary(db, current_user.id)


@router.get("/grade-table")
def get_grade_conversion_table():
    """Lấy bảng quy đổi điểm"""
    return {
        "grade_table": [
            {"score_range": "9.0 - 10.0", "letter_grade": "A", "grade_point": 4.0},
            {"score_range": "8.0 - 8.9", "letter_grade": "B+", "grade_point": 3.5},
            {"score_range": "7.0 - 7.9", "letter_grade": "B", "grade_point": 3.0},
            {"score_range": "6.5 - 6.9", "letter_grade": "C+", "grade_point": 2.5},
            {"score_range": "5.5 - 6.4", "letter_grade": "C", "grade_point": 2.0},
            {"score_range": "5.0 - 5.4", "letter_grade": "D+", "grade_point": 1.5},
            {"score_range": "4.0 - 4.9", "letter_grade": "D", "grade_point": 1.0},
            {"score_range": "< 4.0", "letter_grade": "F", "grade_point": 0.0},
        ],
        "formula": "GPA = Σ(tín_chỉ × điểm_hệ_4) / Σ(tín_chỉ)",
    }
