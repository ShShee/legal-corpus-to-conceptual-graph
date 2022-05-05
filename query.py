query_data = [
    "Người đang hưởng trợ cấp thất nghiệp có được hưởng chế độ bảo hiểm y tế không?",
    "Điều kiện để được hỗ trợ học nghề ?",
    "Hồ sơ xin được hỗ trợ học nghề cần những gì ?",
    "Thủ tục xin hỗ trợ học nghề diễn ra như thế nào ?",
    "Việc chi trả trợ cấp thất nghiệp được quy định như thế nào?",
    "Quy định về thông báo tìm kiếm việc làm trong khi hưởng trợ cấp thất nghiệp là như thế nào ?",
    "Người lao động khi quá tuổi lao động thì có phải đóng bảo hiểm thất nghiệp không ?",
    "Mức hưởng trợ cấp thất nghiệp theo quy định cụ thể được tính như thế nào?",
    "Thời gian hưởng trợ cấp thất nghiệp theo quy định cụ thể được tính như thế nào?",
    "Thời điểm được hưởng trợ cấp thất nghiệp theo quy định cụ thể được tính như thế nào?",
    "Điều kiện để được hưởng trợ cấp thất nghiệp ?",
    "Mức hỗ trợ đào tạo, bồi dưỡng, nâng cao trình độ kỹ năng nghề để duy trì việc làm cho người lao động được quy định như thế nào?",
    "Điều kiện để được hưởng hỗ trợ đào tạo, bồi dưỡng, nâng cao trình độ kỹ năng nghề để duy trì việc làm cho người lao động theo quy định ?",
    "Thời gian hưởng hỗ trợ đào tạo, bồi dưỡng, nâng cao trình độ kỹ năng nghề để duy trì việc làm cho người lao động là bao lâu?",
    "Hồ sơ đề nghị hưởng hỗ trợ đào tạo kỹ năng nghề để duy trì việc làm cho người lao động theo quy định gồm những gì?",
    "Thời gian hưởng hỗ trợ học nghề được quy định như thế nào?",
    "Mức hỗ trợ học nghề được quy định như thế nào?",
    "Tư vấn giới thiệu việc làm đối với người tham gia bảo hiểm thất nghiệp được quy định như thế nào?",
    "Việc hủy hưởng trợ cấp thất nghiệp được quy định như thế nào?",
    "Trường hợp người lao động không đến nhận trợ cấp thất nghiệp được quy định như thế nào?",
    "Hồ sơ đề nghị hưởng trợ cấp thất nghiệp gồm những gì?",
    "Theo quy định của pháp luật về bảo hiểm thất nghiệp hiện nay thì trường hợp nào được ủy quyền cho người khác nộp hồ sơ đề nghị hưởng trợ cấp thất nghiệp qua đường bưu điện?",
    "Những trường hợp nào được ủy quyền cho người khác đến nhận quyết định hưởng trợ cấp thất nghiệp  ?",
    "Việc giải quyết hưởng trợ cấp thất nghiệp được quy định như thế nào?",
    "Thời hạn nộp hồ sơ xin hưởng trợ cấp thất nghiệp theo quy định là bao lâu?",
    "Thời gian đóng bảo hiểm thất nghiệp được tính cụ thể như thế nào?",
    "Đối tượng nào bắt buộc phải tham gia bảo hiểm thất nghiệp theo quy định ?",
    "Có bao nhiêu chế độ bảo hiểm thất nghiệp theo quy định ?",
    "Nguyên tắc của bảo hiểm thất nghiệp theo quy định là như thế nào ?",
    "Hồ sơ tham gia bảo hiểm thất nghiệp gồm những gì ?",
    "Các quy định về tham gia bảo hiểm thất nghiệp cho người lao động là như thế nào? ",
    "Các quy định đóng bảo hiểm thất nghiệp cho người lao động cụ thể ra sao ?",
    "Mức đóng bảo hiểm thất nghiệp theo quy định ?",
    "Trường hợp nào bị tạm dừng việc hưởng trợ cấp thất nghiệp ?",
    "Trường hợp nào được tiếp tục hưởng trợ cấp thất nghiệp ?",
    "Trường hợp nào bị chấm dứt hưởng trợ cấp thất nghiệp ?",
    "Trường hợp nào được bảo lưu thời gian đóng bảo hiểm thất nghiệp ?",
    "Thời gian bảo lưu đóng bảo hiểm thất nghiệp được tính như thế nào ?",
    "Thủ tục và quy trình chuyển nơi hưởng trợ cấp thất nghiệp ?",
    "Quyền của người lao động khi tham gia bảo hiểm thất nghiệp được quy định như thế nào?",
    "Nghĩa vụ của người lao động khi tham gia bảo hiểm thất nghiệp được quy định như thế nào?",
    "Quyền của người sử dụng lao động tham gia bảo hiểm thất nghiệp được quy định như thế nào?",
    "Trách nhiệm của người sử dụng lao động tham gia bảo hiểm thất nghiệp được quy định như thế nào?",
    "Thời gian duyệt hồ sơ xin hưởng trợ cấp thất nghiệp là bao lâu ?",
    "Đối tượng người lao động nào được hưởng hỗ trợ từ quỹ bảo hiểm thất nghiệp do ảnh hưởng bởi dịch COVID-19 ?",
    "Mức hỗ trợ mà người lao động được hưởng từ quỹ bảo hiểm thất nghiệp do ảnh hưởng bởi đại dịch COVID-19 ?",
    "Mức hỗ trợ mà người sử dụng lao động được hưởng từ quỹ bảo hiểm thất nghiệp do ảnh hưởng bởi đại dịch COVID-19 ?",
    "Thủ tục để hưởng trợ cấp từ quỹ bảo hiểm thất nghiệp do ảnh hưởng bởi đại dịch COVID-19 gồm những bước nào ?"
]
