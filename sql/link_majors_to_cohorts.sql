-- Gắn ngành theo khóa học (chạy trên Supabase)
-- K50: Luật tư pháp, Luật hành chính
-- K51: Hóa học
-- COMMON: không gắn khóa

ALTER TABLE majors ADD COLUMN IF NOT EXISTS cohort_id INTEGER REFERENCES cohorts(id);
CREATE INDEX IF NOT EXISTS ix_majors_cohort_id ON majors (cohort_id);

-- Bỏ unique name toàn cục nếu còn (để sau này cùng tên ngành ở khóa khác)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'majors_name_key'
  ) THEN
    ALTER TABLE majors DROP CONSTRAINT majors_name_key;
  END IF;
END $$;

-- Gắn cohort_id theo mã ngành
UPDATE majors
SET cohort_id = (SELECT id FROM cohorts WHERE code = 'K50' LIMIT 1)
WHERE code IN ('LAW', 'LAW_ADMIN');

UPDATE majors
SET cohort_id = (SELECT id FROM cohorts WHERE code = 'K51' LIMIT 1)
WHERE code = 'CHEM';

UPDATE majors
SET cohort_id = NULL
WHERE code = 'COMMON' OR major_type = 'common';

-- Kiểm tra
SELECT m.id, m.code, m.name, m.major_type, c.code AS cohort_code
FROM majors m
LEFT JOIN cohorts c ON c.id = m.cohort_id
ORDER BY m.id;
