from underthesea import word_tokenize, chunk, pos_tag, ner, classify


def reduce_word(input_list, isQuery):
    reduced = []
    for token in input_list:
        if(token[1] == 'N' or token[1] == 'Nc' or token[1] == 'V'):
            reduced.append(token[0])

    result = reduced.copy()

    if(isQuery):
        for idx in range(-3, 0):
            if(reduced[idx].lower() == "là"):
                result.pop(idx)
                if(idx != -1 and (reduced[idx+1].lower() == "như thế nào" or reduced[idx+1].lower() == "bao gồm")):
                    result.pop(idx+1)

    return result


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


def handle_synonyms_in_query(query):
    query_tokenizes = word_tokenize(query)
    result = []
    for idx, val in enumerate(query_tokenizes):
        if((idx+1) < len(query_tokenizes)):
            word_behind = query_tokenizes[idx+1]
        else:
            word_behind = ""
        result.append(convert_synonyms(val.lower(), word_behind.lower()))

    return ' '.join(result)
