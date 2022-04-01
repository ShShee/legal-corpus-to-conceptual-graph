from datasets import tqdm
from underthesea import word_tokenize,chunk,pos_tag,ner,classify
query = 'Quy định về thông báo tìm kiếm việc làm trong khi đang hưởng hỗ trợ từ trợ cấp thất nghiệp là như thế nào ?'

info_1 = 'Thông báo về việc tìm kiếm việc làm khi hưởng trợ cấp thất nghiệp'
info_2 = 'Trường hợp được bỏ qua thông báo về việc tìm kiếm việc làm khi hưởng trợ cấp thất nghiệp'
info_3 = 'Quy định tham gia bảo hiểm thất nghiệp cho người lao động'
info_4 = 'Giải quyết hưởng trợ cấp thất nghiệp'
info_5= 'Thủ tục xin hỗ trợ học nghề'

init_pos_list = []
init_pos_list.append(pos_tag(query))
init_pos_list.append(pos_tag(info_1))
init_pos_list.append(pos_tag(info_2))
init_pos_list.append(pos_tag(info_3))
init_pos_list.append(pos_tag(info_4))
init_pos_list.append(pos_tag(info_5))

def reduce_word(input_list):
    reduced = []
    for token in input_list:
        if(token[1]=='N' or token[1]=='Nc' or token[1]=='V'):
            reduced.append(token)
    return reduced

for item in init_pos_list:
    print("--------- Reduce unnecessary words ------------")
    for token in item:
        print(token)