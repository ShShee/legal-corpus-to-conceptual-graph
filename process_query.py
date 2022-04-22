from underthesea import word_tokenize, chunk, pos_tag, ner, classify


def filter_words(input_list):
    reduced = []
    index = 0
    flag_change_type = False
    while index < len(input_list):
        if index+1 < len(input_list):
            if input_list[index][0] == 'tạm' and input_list[index+1][0] == 'dừng':
                reduced.append(('tạm dừng', 'V'))
                index = index + 2
                continue
            elif input_list[index][0] == 'không' and input_list[index+1][1] == 'V':
                reduced.append(('không '+input_list[index+1][0], 'V'))
                index = index + 2
                continue
            elif input_list[index][0] == 'nâng' and input_list[index+1][0] == 'cao':
                flag_change_type = False
                reduced.append(('nâng cao', 'V'))
                index = index + 2
                continue
            elif (input_list[index][0] == 'kĩ năng' or input_list[index][0] == 'kỹ năng') and input_list[index+1][0] == 'nghề':
                reduced.append(('kỹ năng nghề', 'N'))
                index = index + 2
                continue
            elif input_list[index][0] == 'học' and input_list[index+1][0] == 'nghề':
                flag_change_type = False
                reduced.append(('học nghề', 'N'))
                index = index + 2
                continue
            # elif input_list[index][1] == 'V' and input_list[index+1][1] == 'V':
            #     reduced.append(input_list[index])
            #     flag_change_type = True
            #     index = index + 1
            #     continue

        if input_list[index][1] == 'N' or input_list[index][1] == 'Nc' or input_list[index][1] == 'V':
            # if flag_change_type:
            #     reduced.append((input_list[index][0], 'N'))
            #     flag_change_type = False
            reduced.append(input_list[index])
        index = index + 1

    if reduced and reduced[-1][1] == 'V':
        data = reduced[-1][0]
        reduced.pop()
        reduced.append((data, 'N'))
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
