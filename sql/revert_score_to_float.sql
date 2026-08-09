-- Khôi phục cột điểm về kiểu số nếu trước đó đã ALTER sang TEXT
-- (sau khi tắt mã hóa Fernet trên backend)

ALTER TABLE courses
  ALTER COLUMN score TYPE DOUBLE PRECISION
  USING CASE
    WHEN score ~ '^[0-9]+(\\.[0-9]+)?$' THEN score::double precision
    ELSE 0
  END;

ALTER TABLE courses
  ALTER COLUMN grade_point TYPE DOUBLE PRECISION
  USING CASE
    WHEN grade_point IS NULL THEN NULL
    WHEN grade_point ~ '^[0-9]+(\\.[0-9]+)?$' THEN grade_point::double precision
    ELSE 0
  END;
