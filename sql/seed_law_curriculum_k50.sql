-- Gắn CTĐT Luật tư pháp K50 (chạy sau khi đã có majors + course_catalog)
-- Idempotent: bỏ qua môn đã gắn

-- Đảm bảo ngành Luật tư pháp tồn tại / đổi tên từ "Luật"
INSERT INTO majors (code, name, major_type, description, is_active)
SELECT 'LAW', 'Luật tư pháp', 'specific', 'Ngành Luật tư pháp (K50)', TRUE
WHERE NOT EXISTS (SELECT 1 FROM majors WHERE code = 'LAW');

UPDATE majors
SET name = 'Luật tư pháp',
    description = 'Ngành Luật tư pháp (K50)',
    major_type = 'specific'
WHERE code = 'LAW' OR name = 'Luật';

-- Gắn môn CTĐT theo mã học phần
INSERT INTO curriculum_items (major_id, course_catalog_id)
SELECT m.id, c.id
FROM majors m
JOIN course_catalog c ON c.course_code IN (
  'KL051','ML007','XH028','XH011E','KL233E','KN001E','KN002E',
  'KL101','KL102','KL301','KL302','KL113E','KL105','KL115',
  'KL118','KL119','KL231','KL133','KL131','KL132','KL122',
  'KL123','KL124','KL114','KL116','KL117','KL303','KL304',
  'KL210','KL353','KL365','KL371','KL227','KL327','KL328',
  'KL375','KL376','KL377','KL383','KL385','KL335','KL404',
  'KL386','KL378','KL380E','KL211E','KL212E','KL229E','KL333',
  'KL406','KL344','KL420E','KL370'
)
WHERE m.code = 'LAW'
  AND NOT EXISTS (
    SELECT 1 FROM curriculum_items ci
    WHERE ci.major_id = m.id AND ci.course_catalog_id = c.id
  );
