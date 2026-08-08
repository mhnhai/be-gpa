-- Seed CTĐT Hóa học K51 + bổ sung môn chung trùng với Luật
-- Chạy sau khi đã có majors + course_catalog

-- Đảm bảo ngành Hóa học
INSERT INTO majors (code, name, major_type, description, is_active)
SELECT 'CHEM', 'Hóa học', 'specific', 'Ngành Hóa học (K51)', TRUE
WHERE NOT EXISTS (SELECT 1 FROM majors WHERE code = 'CHEM');

UPDATE majors
SET name = 'Hóa học',
    description = 'Ngành Hóa học (K51)',
    major_type = 'specific'
WHERE code = 'CHEM';

-- Đảm bảo ngành chung
INSERT INTO majors (code, name, major_type, description, is_active)
SELECT 'COMMON', 'Môn học chung', 'common', 'Các môn tất cả sinh viên đều học', TRUE
WHERE NOT EXISTS (SELECT 1 FROM majors WHERE code = 'COMMON' OR major_type = 'common');

-- Thêm môn chung (chính trị + trùng Luật/Hóa)
INSERT INTO curriculum_items (major_id, course_catalog_id)
SELECT m.id, c.id
FROM majors m
JOIN course_catalog c ON c.course_code IN (
  'ML014','ML016','ML018','ML019','ML021',
  'ML007','XH028','KN001E','KN002E'
)
WHERE m.code = 'COMMON'
  AND NOT EXISTS (
    SELECT 1 FROM curriculum_items ci
    WHERE ci.major_id = m.id AND ci.course_catalog_id = c.id
  );

-- CTĐT Hóa học K51 (không gồm mã đã chuyển sang môn chung)
INSERT INTO curriculum_items (major_id, course_catalog_id)
SELECT m.id, c.id
FROM majors m
JOIN course_catalog c ON c.course_code IN (
  'KL001E','XH011','XH012','XH014',
  'TN059','TN044','TN048','TN049','TN042','TN043','TN427E',
  'TN101','TN102','TN103','TN236','TN173','TN247','TN107',
  'TN111','TN112','TN249E','TN178','TN108','TN109','TN110',
  'TN115','TN180','TN117','TN182','TN301','TN163','XH019',
  'TN363','TN364','TN437','TN312','TN438','TN322','TN308',
  'TN309','TN310','TN439','TN292','TN245E','TN319','TN323',
  'TN496E','TN243E','TN452','TN379','TN395E','TN498','TN473',
  'TN465E','TN313E','TN339','TN327E','TN387E','TN300E','TN338'
)
WHERE m.code = 'CHEM'
  AND NOT EXISTS (
    SELECT 1 FROM curriculum_items ci
    WHERE ci.major_id = m.id AND ci.course_catalog_id = c.id
  );
