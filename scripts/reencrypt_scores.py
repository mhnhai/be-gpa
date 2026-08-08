"""
Mã hóa lại toàn bộ score/grade_point đang là plaintext trong DB.
Chạy trên máy có DATABASE_URL + SECRET_KEY trùng Render:

  cd be-gpa
  $env:DATABASE_URL="..."
  $env:SECRET_KEY="..."   # phải trùng SECRET_KEY trên Render
  python scripts/reencrypt_scores.py
"""

from app.db.session import SessionLocal
from app.models.course import Course


def main() -> None:
    db = SessionLocal()
    try:
        courses = db.query(Course).all()
        updated = 0
        for course in courses:
            score = course.score
            gp = course.grade_point
            course.score = float(score)
            if gp is not None:
                course.grade_point = float(gp)
            updated += 1
        db.commit()
        print(f"OK: re-encrypted {updated} courses")
    finally:
        db.close()


if __name__ == "__main__":
    main()
