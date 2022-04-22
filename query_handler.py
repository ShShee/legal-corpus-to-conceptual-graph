from re import S
from turtle import pos
from matplotlib.pyplot import title

from numpy import append
from generate_data import data_type
from process_query import filter_words, check_unnecessaries, convert_synonyms
from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from enums import VariableTypes


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

# def reduce_words(query_data):
#     for item in query_data:
#         query = filter_words(pos_tag(handle_in_query(item)))
#         skip = 0
#         words = []
#         pos_list = []
#         list_query = []
#         start = 0
#         last_checkpoint = ""
#         while start < len(query):
#             list_same_names = []
#             start_next = False
#             while start_next == False:
#                 if skip == 0:
#                     words = [query[start][0]]
#                     pos_list = [query[start][1]]
#                 else:
#                     words.append(query[start][0])
#                     pos_list.append(query[start][1])
#                     skip = skip - 1
#                 for type in data_type:
#                     for name in type.getParentsNames(' '.join(words)):
#                         if(name):
#                             list_same_names.append(name)

#                 count_inclued = len(list_same_names)
#                 if(count_inclued == 0):
#                     if last_checkpoint:
#                         list_query.append((last_checkpoint, 'Np'))
#                         last_checkpoint = ""
#                     else:
#                         list_query.append((words[0], pos_list[0]))
#                         start = start - len(words) + 2
#                         start_next = True
#                 elif (count_inclued == 1 and ' '.join(words) == list_same_names[0]):
#                     last_checkpoint = ""
#                     list_query.append((' '.join(words), 'Np'))
#                     start = start + 1
#                     start_next = True
#                     # else:
#                     #     list_query.append((list_same_names[0], 'Np'))
#                 else:
#                     for name in list_same_names:
#                         if(name == ' '.join(words)):
#                             last_checkpoint = ' '.join(words)
#                     start_next = True
#                     start = start + 1
#                     skip = skip+1

#         print(list_query)


def reduce_words(query_data):
    for item in query_data:
        query = filter_words(pos_tag(handle_in_query(item)))
        skip = 0
        #print(query)
        list_query = []
        start = 0
        while start < len(query):
            list_same_names = []
            if skip != 0:
                skip = skip - 1
            else:
                for type in data_type:
                    namesList = type.getParentsNames(query[start][0])
                    for name in namesList:
                        list_same_names.append(name)

                count_inclued = len(list_same_names)
                if(count_inclued != 0):
                    max_step = -1
                    last_length = -1
                    get_data = ""
                    for item in list_same_names:
                        step, length = getChildLength(
                            query[start][0], item, query)
                        #print(query[start][0], "---", item,"---", step, "+", max_step)
                        if step >= max_step:
                            if (max_step == -1 and step <= 0) or length == -1:
                                get_data = query[start][0]
                            elif (step == max_step and (last_length == -1 or length < last_length)) or max_step != step:
                                get_data = item
                                last_length = length
                            max_step = step
                    skip = max_step if max_step > 0 else 0
                    list_query.append(
                        (get_data, 'Np' if max_step > 0 else query[start][1]))
                else:
                    list_query.append(query[start])
            start = start + 1
        print(list_query)


def getChildLength(title, data, query):
    wordsList = filter_words(pos_tag(data))
    data_types_included = checkVariableTypesIncluded(wordsList)
    start = -1
    end = -1
    for index in range(0, len(query)):
        if(query[index][0] == title):
            start = index
        if (wordsList[-1][0] == query[index][0]):
            end = index
        if end >= start and end != -1 and start != -1:
            break
    #print(start, "///", end, query, wordsList)
    if(end == -1):
        return (-1, -1)
    else:
        step = 0
        appearedWordsList = [query[start]]
        for index in range(start+1, end+1):
            appeared = False
            # print(query[index][0])
            appearedWordsList.append(query[index])
            for item in wordsList:
                #print(item[0], "====", query[index][0])
                if(item[0] == query[index][0]):
                    step = step + 1
                    appeared = True
            if appeared == False:
                #print('Case 1')
                return (0, 0)
        #print(appearedWordsList, "---", checkVariableTypesIncluded(appearedWordsList),'==', wordsList, "---", data_types_included)
        if checkVariableTypesIncluded(appearedWordsList) == data_types_included or len(appearedWordsList) == len(wordsList):
            #print('Case 2')
            return (step, len(appearedWordsList))
        else:
            #print('Case 3')
            return (0, -1)


def checkVariableTypesIncluded(wordsList):
    data_has_verb = False
    data_has_noun = False
    for item in wordsList:
        if not data_has_noun or not data_has_verb:
            if(item[1] == 'V'):
                data_has_verb = True
            elif (item[1] == 'N' or item[1] == 'Nc'):
                data_has_noun = True
        else:
            break

    if data_has_noun and data_has_verb:
        return VariableTypes.BOTH
    elif data_has_verb:
        return VariableTypes.ONLY_VERBS
    elif data_has_noun:
        return VariableTypes.ONLY_NOUNS


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
