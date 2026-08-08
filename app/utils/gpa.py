"""
Bảng quy đổi điểm:
- 9.0 - 10.0: A  -> 4.0
- 8.0 - 8.9:  B+ -> 3.5
- 7.0 - 7.9:  B  -> 3.0
- 6.5 - 6.9:  C+ -> 2.5
- 5.5 - 6.4:  C  -> 2.0
- 5.0 - 5.4:  D+ -> 1.5
- 4.0 - 4.9:  D  -> 1.0
- < 4.0:      F  -> 0.0
"""


def convert_score_to_letter_and_gpa(score: float) -> tuple[str, float]:
    """Chuyển đổi điểm số (thang 10) sang điểm chữ và điểm hệ 4."""
    if score >= 9.0:
        return ("A", 4.0)
    elif score >= 8.0:
        return ("B+", 3.5)
    elif score >= 7.0:
        return ("B", 3.0)
    elif score >= 6.5:
        return ("C+", 2.5)
    elif score >= 5.5:
        return ("C", 2.0)
    elif score >= 5.0:
        return ("D+", 1.5)
    elif score >= 4.0:
        return ("D", 1.0)
    else:
        return ("F", 0.0)


def calculate_gpa(courses: list) -> tuple[float, int]:
    """
    Tính điểm trung bình theo công thức:
    GPA = Σ(ai * Xi) / Σ(ai)
    """
    if not courses:
        return (0.0, 0)

    total_weighted = sum(course.credits * course.grade_point for course in courses)
    total_credits = sum(course.credits for course in courses)

    if total_credits == 0:
        return (0.0, 0)

    gpa = total_weighted / total_credits
    return (round(gpa, 2), total_credits)
