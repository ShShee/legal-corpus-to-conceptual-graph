from underthesea import word_tokenize, chunk, pos_tag, ner, classify


def reduce_word(input_list):
    reduced = []
    for token in input_list:
        if(token[1] == 'N' or token[1] == 'Nc' or token[1] == 'V' or token[0] == 'tạm' or token[0] == 'hủy' or token[0] == 'không'):
            reduced.append(token)

    return reduced


def check_unnecessaries(word, word_behind):
    if((word == 'có' and word_behind == 'được')
       or (word == 'diễn' and word_behind == 'ra')
       or ((word == 'các' or word == 'những') and word_behind == 'bước') or (word == 'không' and (word_behind == '?' or word_behind == ''))):
        return 2
    elif(word == 'như thế nào' or word == 'về' or word == 'phải'
         or word == 'cần' or word == 'tính' or word == 'được'
         or word == 'theo' or word == 'có' or word == 'gồm'
         or word == 'trường hợp' or word == 'bị' or word == 'khi'
         or word == 'là' or word == 'như thế nào'
         or word == 'bao nhiêu' or word == 'bao gồm'):
        return 1
    else:
        return 0


def convert_synonyms(word, word_behind):
    if(word == 'thời hạn'):
        return "thời gian"
    elif(word == 'xử lí' or word == 'xử lý'):
        return "giải quyết"
    elif(word == 'giấy tờ'):
        return "hồ sơ"
    elif(word == 'corona' or word == 'ncov'):
        return "covid-19"
    elif((word == 'xin' or word == 'yêu cầu') and word_behind != 'đề nghị'):
        return "đề nghị"
    elif(word == 'nộp' or word == 'gửi'):
        return "nộp"
    elif(word == 'nhận' and word_behind == 'trợ cấp'):
        return "hưởng"
    else:
        return word


def handle_in_query(query):
    query_tokenizes=word_tokenize(query)
    result=[]
    exclude_next=False
    for idx, val in enumerate(query_tokenizes):
        if exclude_next:
            exclude_next=False
        else:
            if((idx+1) < len(query_tokenizes)):
                word_behind=query_tokenizes[idx+1]
            else:
                word_behind=""

            checked=check_unnecessaries(val.lower(), word_behind.lower())
            if checked != 0:
                exclude_next=True if checked == 2 else False
                continue
            result.append(convert_synonyms(val.lower(), word_behind.lower()))

    return ' '.join(result)
