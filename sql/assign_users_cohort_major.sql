-- Kiểm tra user 1 & 2 đã có khóa học / ngành chưa
SELECT
  u.id,
  u.username,
  u.email,
  u.cohort_id,
  c.code AS cohort_code,
  u.major_id,
  m.code AS major_code,
  m.name AS major_name
FROM users u
LEFT JOIN cohorts c ON c.id = u.cohort_id
LEFT JOIN majors m ON m.id = u.major_id
WHERE u.id IN (1, 2)
ORDER BY u.id;

-- Gán nếu CHƯA có (không ghi đè nếu đã có sẵn)
-- user.id = 1 → K50 + Luật tư pháp
UPDATE users
SET
  cohort_id = COALESCE(cohort_id, (SELECT id FROM cohorts WHERE code = 'K50' LIMIT 1)),
  major_id  = COALESCE(major_id,  (SELECT id FROM majors  WHERE code = 'LAW' LIMIT 1))
WHERE id = 1;

-- user.id = 2 → K51 + Hóa học
UPDATE users
SET
  cohort_id = COALESCE(cohort_id, (SELECT id FROM cohorts WHERE code = 'K51' LIMIT 1)),
  major_id  = COALESCE(major_id,  (SELECT id FROM majors  WHERE code = 'CHEM' LIMIT 1))
WHERE id = 2;

-- Kiểm tra lại sau khi gán
SELECT
  u.id,
  u.username,
  c.code AS cohort_code,
  m.code AS major_code,
  m.name AS major_name
FROM users u
LEFT JOIN cohorts c ON c.id = u.cohort_id
LEFT JOIN majors m ON m.id = u.major_id
WHERE u.id IN (1, 2)
ORDER BY u.id;
