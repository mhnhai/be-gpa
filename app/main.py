import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base, SessionLocal
from .routers import auth, semesters, courses, gpa, catalog
from .seed_catalog import seed_catalog

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed course catalog
def init_db():
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
    version="1.0.0"
)

# CORS configuration - allow frontend origins
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
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
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}

