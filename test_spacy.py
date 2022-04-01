import spacy
nlp = spacy.load('vi_core_news_lg')
query = 'Quy định về tham gia trợ cấp thất nghiệp cho người lao động và thông báo tìm kiếm việc làm trong khi đang hưởng hỗ trợ từ trợ cấp thất nghiệp là như thế nào ?'

info_1 = 'Thông báo về việc tìm kiếm việc làm khi hưởng trợ cấp thất nghiệp'
info_2 = 'Trường hợp được bỏ qua thông báo về việc tìm kiếm việc làm khi hưởng trợ cấp thất nghiệp'
info_3 = 'Quy định tham gia bảo hiểm thất nghiệp cho người lao động'
info_4 = 'Giải quyết hưởng trợ cấp thất nghiệp'
info_5= 'Thủ tục xin hỗ trợ học nghề'

init_pos_list = []
init_pos_list.append(nlp(query))
init_pos_list.append(nlp(info_1))
init_pos_list.append(nlp(info_2))
init_pos_list.append(nlp(info_3))
init_pos_list.append(nlp(info_4))
init_pos_list.append(nlp(info_5))

def reduce_word(input_list):
    reduced = []
    for token in input_list:
        if(token.tag_=='N' or token.tag_=='Nc' or token.tag_=='V'):
            reduced.append(token)
    return reduced

for item in init_pos_list:
    print("--------- Reduce unnecessary words ------------")
    for token in reduce_word(item):
        print(token.text,token.tag_,sep=",")