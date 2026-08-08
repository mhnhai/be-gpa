"""Seed khóa học, ngành học (chung/riêng) và CTĐT.

Quy tắc môn chung: chỉ những mã xuất hiện trong CẢ 3 CTĐT
(Luật tư pháp K50, Luật hành chính K50, Hóa học K51).
"""

from sqlalchemy.orm import Session

from app.models.catalog import CourseCatalog
from app.models.cohort import Cohort
from app.models.curriculum import CurriculumItem
from app.models.major import Major

DEFAULT_COHORTS = [
    ("K48", "Khóa 48"),
    ("K49", "Khóa 49"),
    ("K50", "Khóa 50"),
    ("K51", "Khóa 51"),
    ("K52", "Khóa 52"),
]

DEFAULT_MAJORS = [
    ("COMMON", "Môn học chung", "common", "Môn trùng cả 3 CTĐT (Luật tư pháp, Luật hành chính, Hóa học)"),
    ("LAW", "Luật tư pháp", "specific", "Ngành Luật tư pháp (K50)"),
    ("LAW_ADMIN", "Luật hành chính", "specific", "Ngành Luật hành chính (K50)"),
    ("CHEM", "Hóa học", "specific", "Ngành Hóa học (K51)"),
]

# CTĐT gốc Luật tư pháp K50
LAW_JUDICIAL_FULL = [
    "KL051", "ML007", "XH028", "XH011E", "KL233E", "KN001E", "KN002E",
    "KL101", "KL102", "KL301", "KL302", "KL113E", "KL105", "KL115",
    "KL118", "KL119", "KL231", "KL133", "KL131", "KL132", "KL122",
    "KL123", "KL124", "KL114", "KL116", "KL117", "KL303", "KL304",
    "KL210", "KL353", "KL365", "KL371", "KL227", "KL327", "KL328",
    "KL375", "KL376", "KL377", "KL383", "KL385", "KL335", "KL404",
    "KL386", "KL378", "KL380E", "KL211E", "KL212E", "KL229E", "KL333",
    "KL406", "KL344", "KL420E", "KL370",
]

# CTĐT gốc Luật hành chính K50
LAW_ADMIN_FULL = [
    "KL051", "ML007", "XH028", "XH011E", "KL233E", "KN001E", "KN002E",
    "KL101", "KL102", "KL301", "KL302", "KL113E", "KL105", "KL115",
    "KL118", "KL119", "KL231", "KL133", "KL131", "KL132", "KL122",
    "KL123", "KL124", "KL114", "KL116", "KL117", "KL303", "KL304",
    "KL210", "KL353", "KL365", "KL371", "KL227", "KL327", "KL328",
    "KL375", "KL376", "KL377", "KL383", "KL385", "KL335", "KL404",
    "KL386", "KL378", "KL380E", "KL211E", "KL212E", "KL229E", "KL333",
    "KL406", "KL344", "KL420E", "KL370",
]

# CTĐT gốc Hóa học K51
CHEM_FULL = [
    "KL001E", "ML007", "XH028", "XH011", "XH012", "XH014", "KN001E", "KN002E",
    "TN059", "TN044", "TN048", "TN049", "TN042", "TN043", "TN427E",
    "TN101", "TN102", "TN103", "TN236", "TN173", "TN247", "TN107",
    "TN111", "TN112", "TN249E", "TN178", "TN108", "TN109", "TN110",
    "TN115", "TN180", "TN117", "TN182", "TN301", "TN163", "XH019",
    "TN363", "TN364", "TN437", "TN312", "TN438", "TN322", "TN308",
    "TN309", "TN310", "TN439", "TN292", "TN245E", "TN319", "TN323",
    "TN496E", "TN243E", "TN452", "TN379", "TN395E", "TN498", "TN473",
    "TN465E", "TN313E", "TN339", "TN327E", "TN387E", "TN300E", "TN338",
]

# Chỉ mã nằm trong CẢ 3 CTĐT
COMMON_COURSE_CODES = sorted(
    set(LAW_JUDICIAL_FULL) & set(LAW_ADMIN_FULL) & set(CHEM_FULL)
)
# => ML007, XH028, KN001E, KN002E

LAW_JUDICIAL_COURSE_CODES = [c for c in LAW_JUDICIAL_FULL if c not in COMMON_COURSE_CODES]
LAW_ADMIN_COURSE_CODES = [c for c in LAW_ADMIN_FULL if c not in COMMON_COURSE_CODES]
CHEM_COURSE_CODES = [c for c in CHEM_FULL if c not in COMMON_COURSE_CODES]


def _add_courses_to_major(db: Session, major: Major, course_codes: list[str]) -> int:
    added = 0
    for code in course_codes:
        course = (
            db.query(CourseCatalog)
            .filter(CourseCatalog.course_code == code)
            .first()
        )
        if not course:
            print(f"⚠️  Bỏ qua mã chưa có trong catalog: {code}")
            continue
        exists = (
            db.query(CurriculumItem)
            .filter(
                CurriculumItem.major_id == major.id,
                CurriculumItem.course_catalog_id == course.id,
            )
            .first()
        )
        if exists:
            continue
        db.add(
            CurriculumItem(
                major_id=major.id,
                course_catalog_id=course.id,
            )
        )
        added += 1
    if added:
        db.commit()
    return added


def seed_cohorts(db: Session) -> int:
    added = 0
    for code, name in DEFAULT_COHORTS:
        existing = db.query(Cohort).filter(Cohort.code == code).first()
        if existing:
            continue
        db.add(Cohort(code=code, name=name, is_active=True))
        added += 1
    if added:
        db.commit()
    return added


def seed_majors(db: Session) -> int:
    added = 0
    for code, name, major_type, description in DEFAULT_MAJORS:
        existing = db.query(Major).filter(Major.code == code).first()
        if existing:
            if (
                existing.name != name
                or existing.description != description
                or existing.major_type != major_type
            ):
                existing.name = name
                existing.description = description
                existing.major_type = major_type
                db.commit()
            continue

        by_name = db.query(Major).filter(Major.name == name).first()
        if by_name:
            by_name.code = code
            by_name.major_type = major_type
            by_name.description = description
            db.commit()
            continue

        if code == "LAW":
            old = db.query(Major).filter(Major.name == "Luật").first()
            if old:
                old.name = name
                old.code = code
                old.major_type = major_type
                old.description = description
                db.commit()
                continue

        db.add(
            Major(
                code=code,
                name=name,
                major_type=major_type,
                description=description,
                is_active=True,
            )
        )
        added += 1

    if added:
        db.commit()
    return added


def _get_major(db: Session, code: str, name: str) -> Major | None:
    return (
        db.query(Major).filter(Major.code == code).first()
        or db.query(Major).filter(Major.name == name).first()
    )


def seed_common_curriculum(db: Session) -> int:
    major = _get_major(db, "COMMON", "Môn học chung")
    if not major:
        return 0
    return _add_courses_to_major(db, major, COMMON_COURSE_CODES)


def seed_law_curriculum(db: Session) -> int:
    major = _get_major(db, "LAW", "Luật tư pháp")
    if not major:
        return 0
    return _add_courses_to_major(db, major, LAW_JUDICIAL_COURSE_CODES)


def seed_law_admin_curriculum(db: Session) -> int:
    major = _get_major(db, "LAW_ADMIN", "Luật hành chính")
    if not major:
        return 0
    return _add_courses_to_major(db, major, LAW_ADMIN_COURSE_CODES)


def seed_chem_curriculum(db: Session) -> int:
    major = _get_major(db, "CHEM", "Hóa học")
    if not major:
        return 0
    return _add_courses_to_major(db, major, CHEM_COURSE_CODES)


def seed_academic_structure(db: Session) -> dict:
    return {
        "cohorts": seed_cohorts(db),
        "majors": seed_majors(db),
        "common_curriculum": seed_common_curriculum(db),
        "law_curriculum": seed_law_curriculum(db),
        "law_admin_curriculum": seed_law_admin_curriculum(db),
        "chem_curriculum": seed_chem_curriculum(db),
    }
