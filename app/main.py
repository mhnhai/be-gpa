from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import Course, CourseCatalog, Semester, User  # noqa: F401
from app.routers import auth, catalog, courses, gpa, semesters
from app.seed.catalog import seed_catalog

# Create database tables
Base.metadata.create_all(bind=engine)


def init_db() -> None:
    db = SessionLocal()
    try:
        added = seed_catalog(db)
        if added > 0:
            print(f"✅ Đã thêm {added} môn học vào kho")
    finally:
        db.close()


init_db()

app = FastAPI(
    title="GPA Calculator API",
    description="API để tính điểm trung bình tích lũy (GPA) cho sinh viên",
    version="1.0.0",
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
