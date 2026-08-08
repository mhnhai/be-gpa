-- Đổi kiểu cột điểm sang TEXT để lưu giá trị đã mã hóa (Fernet)
-- App sẽ tự mã hóa khi ghi mới / cập nhật; dữ liệu số cũ vẫn đọc được tạm thời.

ALTER TABLE courses
  ALTER COLUMN score TYPE TEXT USING score::text;

ALTER TABLE courses
  ALTER COLUMN grade_point TYPE TEXT USING grade_point::text;
