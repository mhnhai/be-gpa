from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import (  # noqa: F401
    Cohort,
    Course,
    CourseCatalog,
    CurriculumItem,
    Major,
    PasswordResetOTP,
    Semester,
    User,
)
from app.routers import (
    auth,
    catalog,
    cohorts,
    courses,
    curriculum,
    gpa,
    majors,
    semesters,
)
from app.seed.academic import seed_academic_structure
from app.seed.catalog import seed_catalog

# Create database tables
Base.metadata.create_all(bind=engine)


def init_db() -> None:
    db = SessionLocal()
    try:
        catalog_added = seed_catalog(db)
        if catalog_added > 0:
            print(f"✅ Đã thêm/cập nhật {catalog_added} môn học vào kho")

        academic = seed_academic_structure(db)
        if academic["cohorts"]:
            print(f"✅ Đã thêm {academic['cohorts']} khóa học")
        if academic["majors"]:
            print(f"✅ Đã thêm {academic['majors']} ngành học")
        if academic["common_curriculum"]:
            print(f"✅ Đã gắn {academic['common_curriculum']} môn vào CTĐT chung")
        if academic.get("law_curriculum"):
            print(f"✅ Đã gắn {academic['law_curriculum']} môn vào CTĐT Luật tư pháp")
        if academic.get("law_admin_curriculum"):
            print(f"✅ Đã gắn {academic['law_admin_curriculum']} môn vào CTĐT Luật hành chính")
        if academic.get("chem_curriculum"):
            print(f"✅ Đã gắn {academic['chem_curriculum']} môn vào CTĐT Hóa học")

    finally:
        db.close()


init_db()

app = FastAPI(
    title="GPA Calculator API",
    description="API để tính điểm trung bình tích lũy (GPA) cho sinh viên",
    version="1.1.0",
)

allowed_origins = [
    origin.strip()
    for origin in settings.ALLOWED_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(semesters.router)
app.include_router(courses.router)
app.include_router(gpa.router)
app.include_router(catalog.router)
app.include_router(cohorts.router)
app.include_router(majors.router)
app.include_router(curriculum.router)


@app.get("/")
def root():
    return {
        "message": "Chào mừng đến với GPA Calculator API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
