"""Script để thêm dữ liệu môn học vào kho"""

COURSE_CATALOG = [
    # Môn chung
    ("ML014", "Triết học Mác - Lênin", 3),
    ("ML016", "Kinh tế chính trị Mác - Lênin", 2),
    ("ML018", "Chủ nghĩa xã hội khoa học", 2),
    ("ML019", "Lịch sử Đảng Cộng sản Việt Nam", 2),
    ("ML021", "Tư tưởng Hồ Chí Minh", 2),
    ("KL051", "Quyền con người", 2),
    ("ML007", "Logic học đại cương", 2),
    ("XH028", "Xã hội học đại cương", 2),
    ("XH011E", "Cơ sở văn hóa Việt Nam", 2),
    ("KL233E", "Học thuyết pháp lý", 2),
    ("KN001E", "Kỹ năng mềm", 2),
    ("KN002E", "Đổi mới sáng tạo và khởi nghiệp", 2),
    
    # Môn cơ sở ngành
    ("KL101", "Lý luận nhà nước và pháp luật 1", 2),
    ("KL102", "Lý luận nhà nước và pháp luật 2", 2),
    ("KL301", "Luật hiến pháp 1", 2),
    ("KL302", "Luật hiến pháp 2", 2),
    ("KL113E", "Lịch sử nhà nước và pháp luật", 2),
    ("KL105", "Luật so sánh", 2),
    ("KL115", "Phương pháp nghiên cứu khoa học - Luật", 2),
    
    # Luật hình sự
    ("KL118", "Luật hình sự phần chung", 2),
    ("KL119", "Luật hình sự phần riêng", 2),
    
    # Luật dân sự
    ("KL231", "Luật dân sự: Chủ thể, tài sản, quyền sở hữu và quyền thừa kế", 2),
    ("KL133", "Luật dân sự: Nghĩa vụ dân sự", 2),
    
    # Pháp luật thương mại
    ("KL131", "Pháp luật thương mại 1", 2),
    ("KL132", "Pháp luật thương mại 2", 2),
    
    # Các môn luật khác
    ("KL122", "Luật hôn nhân và gia đình", 2),
    ("KL123", "Luật lao động", 3),
    ("KL124", "Luật tài chính nhà nước", 3),
    ("KL114", "Soạn thảo văn bản pháp luật", 2),
    ("KL116", "Thuật ngữ pháp lý - Tiếng Anh", 2),
    ("KL117", "Thuật ngữ pháp lý - Tiếng Pháp", 2),
    
    # Luật hành chính
    ("KL303", "Luật hành chính 1", 2),
    ("KL304", "Luật hành chính 2", 2),
    ("KL378", "Luật hành chính 3", 2),
    ("KL210", "Pháp luật về quy hoạch và giải phóng mặt bằng", 2),
    ("KL353", "Pháp luật về khiếu nại và khiếu kiện hành chính", 2),
    ("KL365", "Pháp luật về thanh tra", 2),
    
    # Tố tụng
    ("KL371", "Luật tố tụng hình sự", 2),
    ("KL227", "Pháp luật tố tụng dân sự", 3),
    
    # Luật đất đai, môi trường
    ("KL327", "Luật đất đai", 3),
    ("KL328", "Luật môi trường", 2),
    ("KL420E", "Pháp luật về giá đất", 2),
    ("KL423E", "Pháp luật về thanh tra đất đai", 2),
    
    # Công pháp, tư pháp quốc tế
    ("KL375", "Công pháp quốc tế", 3),
    ("KL376", "Tư pháp quốc tế", 3),
    
    # Luật xây dựng, nhà ở
    ("KL377", "Pháp luật về xây dựng", 2),
    ("KL386", "Pháp luật về nhà ở", 2),
    ("KL385", "Thủ tục hành chính về nhà đất", 2),
    
    # Quản lý nhà nước
    ("KL383", "Quản lý nhà nước về hộ tịch", 2),
    ("KL418E", "Quản lý nhà nước về đô thị và nông thôn", 2),
    ("KL382E", "Tổ chức công sở và nhân sự hành chính", 2),
    
    # Sở hữu trí tuệ, hợp đồng
    ("KL335", "Pháp luật về sở hữu trí tuệ", 2),
    ("KL404", "Luật hợp đồng thông dụng", 2),
    ("KL344", "Bảo đảm nghĩa vụ", 2),
    
    # Luật an sinh, lao động
    ("KL380E", "Luật an sinh xã hội", 2),
    
    # Luật nước ngoài
    ("KL211E", "Luật hiến pháp nước ngoài", 2),
    ("KL212E", "Luật hành chính các nước", 2),
    ("KL229E", "Luật hiến pháp chuyên sâu", 2),
    
    # Luật thương mại quốc tế
    ("KL333", "Luật thương mại quốc tế", 2),
    
    # Thực hành, nghiệp vụ
    ("KL406", "Thực hành nghề Luật", 2),
    ("KL397", "Nghiệp vụ tòa án", 2),
    ("KL419", "Kỹ thuật soạn thảo văn bản hành chính", 2),
    ("KL421E", "Các hoạt động hành chính tư pháp", 2),
    ("KL422E", "Xử phạt vi phạm hành chính trong một số lĩnh vực", 2),
    
    # Tốt nghiệp - Luật
    ("KL370", "Luận văn tốt nghiệp - Luật", 10),
    ("KL411", "Tiểu luận tốt nghiệp - Luật", 4),
    ("KL431", "Thực tập tốt nghiệp", 2),
    
    # ========== NGÀNH HÓA HỌC ==========
    
    # Môn chung bổ sung
    ("KL001E", "Pháp luật đại cương", 2),
    ("XH011", "Cơ sở văn hóa Việt Nam", 2),
    ("XH012", "Tiếng Việt thực hành", 2),
    ("XH014", "Văn bản và lưu trữ học đại cương", 2),
    
    # Toán, Lý, Sinh
    ("TN059", "Toán cao cấp B", 3),
    ("TN044", "Xác suất thống kê B", 2),
    ("TN048", "Vật lý đại cương", 3),
    ("TN049", "TT. Vật lý đại cương", 1),
    ("TN042", "Sinh học đại cương", 2),
    ("TN043", "TT. Sinh học đại cương", 1),
    ("TN427E", "An toàn và quản lý phòng thí nghiệm", 2),
    
    # Hóa học đại cương
    ("TN101", "Hóa học đại cương 1", 2),
    ("TN102", "Hóa học đại cương 2", 3),
    ("TN103", "TT. Hóa học đại cương 2", 1),
    
    # Hóa vô cơ
    ("TN236", "Hóa vô cơ 1", 3),
    ("TN173", "TT. Hóa vô cơ 1", 1),
    ("TN247", "Hóa vô cơ 2", 3),
    ("TN107", "TT. Hóa vô cơ 2", 1),
    ("TN465E", "Hóa vô cơ sinh hóa", 2),
    
    # Hóa hữu cơ
    ("TN111", "Hóa hữu cơ 1", 3),
    ("TN112", "TT. Hóa hữu cơ 1", 1),
    ("TN249E", "Hóa hữu cơ 2", 3),
    ("TN178", "TT. Hóa hữu cơ 2", 1),
    ("TN327E", "Tổng hợp hữu cơ", 2),
    ("TN387E", "Tổng hợp bất đối xứng", 2),
    
    # Hóa lý
    ("TN108", "Hóa lý 1", 3),
    ("TN109", "Hóa lý 2", 3),
    ("TN110", "TT. Hóa lý", 2),
    
    # Hóa phân tích
    ("TN115", "Hóa phân tích 1", 3),
    ("TN180", "TT. Hóa phân tích 1", 1),
    ("TN117", "Hóa phân tích 2", 3),
    ("TN182", "TT. Hóa phân tích 2", 1),
    ("TN438", "Phân tích kỹ thuật", 3),
    ("TN322", "TT. Phân tích kỹ thuật", 1),
    ("TN308", "Các phương pháp phân tích hiện đại", 3),
    ("TN309", "TT. Các phương pháp phân tích hiện đại", 1),
    ("TN292", "Các phương pháp phân tích không hủy mẫu", 2),
    ("TN323", "Các phương pháp thống kê hóa học", 2),
    
    # Hóa lượng tử, phổ nghiệm
    ("TN301", "Hóa lượng tử đại cương", 2),
    ("TN310", "Các phương pháp phổ nghiệm hữu cơ", 3),
    
    # Anh văn, Pháp văn chuyên ngành
    ("TN163", "Anh văn chuyên môn - Hóa học", 2),
    ("XH019", "Pháp văn chuyên môn - KH&CN", 2),
    
    # Hóa sinh
    ("TN363", "Hóa sinh học", 2),
    ("TN364", "TT. Hóa sinh học", 1),
    
    # Hóa môi trường
    ("TN437", "Hóa môi trường", 3),
    ("TN312", "TT. Hóa môi trường", 1),
    ("TN339", "Độc chất học môi trường", 2),
    
    # Kiểm nghiệm
    ("TN439", "Kiểm nghiệm dược phẩm và thực phẩm", 3),
    ("TN245E", "Phương pháp phân tích độc chất và kháng sinh trong động thực vật", 2),
    
    # Hóa học hợp chất thiên nhiên
    ("TN243E", "Hóa học dược liệu", 2),
    ("TN452", "Hóa học hợp chất thiên nhiên", 3),
    ("TN379", "TT. Hóa học hợp chất thiên nhiên", 1),
    ("TN395E", "Kỹ thuật tách chiết hợp chất thiên nhiên", 2),
    
    # Vật liệu nano
    ("TN498", "Kỹ thuật vật liệu nano", 3),
    ("TN473", "TT. Tổng hợp vật liệu nano", 1),
    
    # Tin học, ứng dụng
    ("TN313E", "Tin học ứng dụng trong hóa học", 2),
    ("TN300E", "Hóa học ứng dụng", 2),
    
    # Phương pháp nghiên cứu
    ("TN496E", "Phương pháp nghiên cứu khoa học - Hóa học", 2),
    ("TN319", "Tham quan thực tế", 1),
    
    # Hóa dược
    ("TN455", "Tổng hợp Hóa dược", 3),
    ("TN381", "TT. Tổng hợp Hóa dược", 1),
    ("TN367E", "Hóa dược", 3),
    ("TN522", "Bào chế và sinh dược học", 3),
    ("TN523", "TT. Bào chế và sinh dược học", 1),
    ("TN384E", "Thử nghiệm sinh học", 2),
    ("TN435", "TT. Thử nghiệm sinh học", 1),
    
    # Hóa thực phẩm
    ("NS318", "Hóa học thực phẩm", 3),
    
    # Vật liệu y sinh
    ("TN461E", "Vật liệu y sinh", 2),
    ("TN500", "TT. Vật liệu y sinh", 1),
    
    # Tốt nghiệp - Hóa học
    ("TN338", "Luận văn tốt nghiệp - Hóa học", 10),
    ("TN246", "Tiểu luận tốt nghiệp - Hóa học", 4),
    ("TN575", "Thực tập cơ sở - Hóa học", 6),
]


def seed_catalog(db):
    """Thêm dữ liệu môn học vào database"""
    from .models import CourseCatalog
    
    added = 0
    updated = 0
    
    for course_code, course_name, credits in COURSE_CATALOG:
        # Check if course already exists
        existing = db.query(CourseCatalog).filter(
            CourseCatalog.course_code == course_code
        ).first()
        
        if existing:
            # Update if name or credits changed
            if existing.course_name != course_name or existing.credits != credits:
                existing.course_name = course_name
                existing.credits = credits
                updated += 1
        else:
            new_course = CourseCatalog(
                course_code=course_code,
                course_name=course_name,
                credits=credits,
                is_active=True
            )
            db.add(new_course)
            added += 1
    
    db.commit()
    
    if added > 0:
        print(f"✅ Đã thêm {added} môn học mới vào kho")
    if updated > 0:
        print(f"✅ Đã cập nhật {updated} môn học trong kho")
    
    return added + updated
