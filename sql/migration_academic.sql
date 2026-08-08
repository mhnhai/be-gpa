-- Migration: khóa học, ngành học, CTĐT
-- Chạy trong Supabase SQL Editor nếu bảng users đã tồn tại
-- (create_all chỉ tạo bảng mới, không tự thêm cột users)

CREATE TABLE IF NOT EXISTS cohorts (
  id SERIAL PRIMARY KEY,
  code VARCHAR UNIQUE NOT NULL,
  name VARCHAR,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_cohorts_id ON cohorts (id);
CREATE INDEX IF NOT EXISTS ix_cohorts_code ON cohorts (code);

CREATE TABLE IF NOT EXISTS majors (
  id SERIAL PRIMARY KEY,
  name VARCHAR UNIQUE NOT NULL,
  code VARCHAR UNIQUE,
  major_type VARCHAR NOT NULL DEFAULT 'specific',
  description VARCHAR,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_majors_id ON majors (id);
CREATE INDEX IF NOT EXISTS ix_majors_code ON majors (code);

CREATE TABLE IF NOT EXISTS curriculum_items (
  id SERIAL PRIMARY KEY,
  major_id INTEGER NOT NULL REFERENCES majors(id),
  course_catalog_id INTEGER NOT NULL REFERENCES course_catalog(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT uq_major_course UNIQUE (major_id, course_catalog_id)
);
CREATE INDEX IF NOT EXISTS ix_curriculum_items_id ON curriculum_items (id);
CREATE INDEX IF NOT EXISTS ix_curriculum_items_major_id ON curriculum_items (major_id);
CREATE INDEX IF NOT EXISTS ix_curriculum_items_course_catalog_id ON curriculum_items (course_catalog_id);

ALTER TABLE users ADD COLUMN IF NOT EXISTS cohort_id INTEGER REFERENCES cohorts(id);
ALTER TABLE users ADD COLUMN IF NOT EXISTS major_id INTEGER REFERENCES majors(id);
CREATE INDEX IF NOT EXISTS ix_users_cohort_id ON users (cohort_id);
CREATE INDEX IF NOT EXISTS ix_users_major_id ON users (major_id);
