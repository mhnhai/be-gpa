from sqlalchemy.orm import Session

from app.models.catalog import CourseCatalog
from app.seed.catalog_data import COURSE_CATALOG


def seed_catalog(db: Session) -> int:
    """Thêm dữ liệu môn học vào database"""
    added = 0
    updated = 0

    for course_code, course_name, credits in COURSE_CATALOG:
        existing = (
            db.query(CourseCatalog)
            .filter(CourseCatalog.course_code == course_code)
            .first()
        )

        if existing:
            if existing.course_name != course_name or existing.credits != credits:
                existing.course_name = course_name
                existing.credits = credits
                updated += 1
        else:
            db.add(
                CourseCatalog(
                    course_code=course_code,
                    course_name=course_name,
                    credits=credits,
                    is_active=True,
                )
            )
            added += 1

    db.commit()

    if added > 0:
        print(f"✅ Đã thêm {added} môn học mới vào kho")
    if updated > 0:
        print(f"✅ Đã cập nhật {updated} môn học trong kho")

    return added + updated
