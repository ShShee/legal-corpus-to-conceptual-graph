from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from generate_data import data_type


def reduce_word(input_list):
    reduced = []
    for index in range(0, len(input_list)):
        if input_list[index][1] == 'N' or input_list[index][1] == 'Nc' or input_list[index][1] == 'V' or input_list[index][0] == 'cao':
            reduced.append(input_list[index])
        elif index+1 < len(input_list):
            if input_list[index][0] == 'tạm' and input_list[index+1][0] == 'dừng':
                reduced.append(('tạm dừng', 'V'))
            elif input_list[index][0] == 'không' and input_list[index+1][1] == 'V':
                reduced.append(('không '+input_list[index+1][0], 'V'))
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
         or word == 'bao nhiêu' or word == 'bao gồm' or word == 'hiện nay'):
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
    query_tokenizes = word_tokenize(query)
    result = []
    exclude_next = False
    for idx, val in enumerate(query_tokenizes):
        if exclude_next:
            exclude_next = False
        else:
            if((idx+1) < len(query_tokenizes)):
                word_behind = query_tokenizes[idx+1]
            else:
                word_behind = ""

            checked = check_unnecessaries(val.lower(), word_behind.lower())
            if checked != 0:
                exclude_next = True if checked == 2 else False
                continue
            result.append(convert_synonyms(val.lower(), word_behind.lower()))

    return ' '.join(result)


def define_connection(word_1, word_2):
    type_of_connection = ""
    if(word_2[1] == 'V'):
        for item in data_type:
            value = item.getConntectorType(word_1[0])
            if value:
                type_of_connection = value
        if type_of_connection == 'người':
            return 'tác nhân'
        else:
            return 'ngữ cảnh'
    else:
        for item in data_type:
            value = item.getConntectorType(word_2[0])
            if value:
                type_of_connection = value
        if not type_of_connection:
            return 'đối tượng'
        else:
            return type_of_connection