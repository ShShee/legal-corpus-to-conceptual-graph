from dataType import DataType

data_type = [
    DataType("bảo hiểm", [
        DataType("bảo hiểm thất nghiệp", [
            DataType("trợ cấp thất nghiệp"),
            DataType("hỗ trợ tư vấn, giới thiệu việc làm"),
            DataType("hỗ trợ học nghề"),
            DataType("hỗ trợ đào tạo, bồi dưỡng, nâng cao trình độ kỹ năng nghề")
        ]),
        DataType("bảo hiểm y tế")
    ], True),
    DataType("pháp luật", [
        DataType("quy định")
    ], True),
    DataType("người", [
        DataType("người lao động"),
        DataType("người sử dụng lao động")
    ], True)
]

# for item in data_type:
#     print("Is that included ?", item.isIncluded("hỗ trợ học nghề"))
