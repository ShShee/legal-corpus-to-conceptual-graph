from platform import mac_ver
from re import S
from turtle import pos
from unittest import result
from matplotlib.pyplot import title

from numpy import append
from data_initiation import data
from process_query import filter_words, check_unnecessaries, convert_synonyms
from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from enums import AdditionScores, VariableTypes


def handle_in_query(query):
    query_tokenizes = word_tokenize(query)
    result = []
    exclude_next = False
    for idx, val in enumerate(query_tokenizes):
        if exclude_next:
            exclude_next = False
        else:
            if idx-1 != -1:
                word_previous = query_tokenizes[idx-1]
            else:
                word_previous = ""

            if idx+1 < len(query_tokenizes):
                word_behind = query_tokenizes[idx+1]
            else:
                word_behind = ""

            checked = check_unnecessaries(
                val.lower(), word_previous.lower(), word_behind.lower())
            if checked != 0:
                exclude_next = True if checked == 2 else False
                continue
            result.append(convert_synonyms(
                val.lower(), word_previous.lower(), word_behind.lower()))

    return ' '.join(result)


def define_connection(input_query):
    #print(pos_tag(handle_in_query(input_query)))
    new_query = readd_adverbs(input_query)
    result = []
    first_intent = -1
    main_verb = -1
    idx = 0
    first_action = -1  # position of first verb that trigger has done
    while idx < len(new_query):
        start = idx
        end = -1
        connector = AdditionScores.NONE
        #print('Item:', new_query[idx])
        if idx + 1 < len(new_query):
            if new_query[idx][1] != 'AD':
                if new_query[idx+1][1] == 'AD':
                    end = idx + 2
                else:
                    end = idx + 1
            if end >= len(new_query):
                break

            if checkConditionType(new_query[idx][1]):
                if new_query[idx+1][0] == 'không' and idx + 2 < len(new_query) and new_query[idx+2][1] == 'V' and first_action == -1:
                    connector = AdditionScores.TRIGGER_NOT
                    first_action = idx + 2
                    idx = idx + 1
                elif new_query[end][1] == 'V' and first_action == -1:
                    connector = AdditionScores.TRIGGER
                    first_action = end
                elif checkConditionType(new_query[end][1]):
                    connector = AdditionScores.UNDEFINED
                else:
                    end = -1
            elif new_query[idx][1] == 'V':
                if idx - 1 >= 0:
                    tag = AdditionScores.NONE
                    if checkConditionTarget(new_query[idx-1][0]):
                        tag = AdditionScores.TARGET_ACTION
                    elif checkConditionTheme(new_query[idx-1][0]):
                        tag = AdditionScores.THEME_ACTION

                    if tag != AdditionScores.NONE and new_query[first_action][0] != new_query[idx][0]:
                        result.append(
                            (new_query[first_action], new_query[idx], tag))

                if new_query[end][1] != 'V':
                    for i in range(idx-1, 0, -1):
                        if checkConditionTarget(new_query[i][0]):
                            connector = AdditionScores.INTENT
                            break
                        elif checkConditionTheme(new_query[i][0]):
                            connector = AdditionScores.SITUATION
                            break

                if (checkConditionTarget(new_query[idx+1][0]) or checkConditionTheme(new_query[idx+1][0])) and idx + 2 < len(new_query) and new_query[idx + 2][1] == 'V':
                    end = -1
                    connector = AdditionScores.UNDEFINED

                if connector == AdditionScores.NONE:
                    for i in range(idx+1, len(new_query)):
                        if checkConditionTarget(new_query[i][0]):
                            if checkConditionType(new_query[end][1]):
                                connector = AdditionScores.SITUATION
                            elif new_query[end][1] == 'V':
                                connector = AdditionScores.THEME_ACTION
                            break
                        elif checkConditionTheme(new_query[i][0]):
                            if checkConditionType(new_query[end][1]):
                                connector = AdditionScores.INTENT
                            elif new_query[end][1] == 'V':
                                connector = AdditionScores.TARGET_ACTION
                            break

                if connector == AdditionScores.NONE:
                    #end = -1
                    if checkConditionType(new_query[end][1]):
                        connector = AdditionScores.INTENT
                    elif new_query[end][1] == 'V':
                        connector = AdditionScores.TARGET_ACTION
        if end >= 0:
            if connector == AdditionScores.INTENT:
                first_intent = end
                main_verb = idx
            result.append(
                (new_query[start], new_query[end], connector))

        idx = idx + 1

    # start connect main verb to all nouns behind it
    if main_verb != -1:
        for i in range(first_intent + 1, len(new_query)):
            if checkConditionType(new_query[i][1]):
                result.append(
                    (new_query[main_verb], new_query[i], AdditionScores.INTENT_EXTRA))

    #print(recheckConditions(result))
    return (recheckConditions(result), new_query)


def recheckConditions(result):
    new_result = []

    theme_flag = -1
    target_flag = -1

    for idx in range(len(result)-1, 0, -1):
        if (result[idx][2] == AdditionScores.SITUATION or result[idx][2] == AdditionScores.THEME_ACTION) and theme_flag == -1:
            theme_flag = idx
        elif (result[idx][2] == AdditionScores.INTENT or result[idx][2] == AdditionScores.TARGET_ACTION) and target_flag == -1:
            target_flag = idx

        if target_flag != -1 and theme_flag != -1:
            break

    for idx, item in enumerate(result):
        if item[2] == AdditionScores.UNDEFINED and item[1][1] == 'N' and item[0][1] == 'N':
            new_result.append((item[0], item[1], AdditionScores.TARGET_EVENT if (target_flag < theme_flag and idx <
                               theme_flag) or (target_flag > theme_flag and idx >
                               theme_flag) or theme_flag == -1 else AdditionScores.THEME_EVENT))
        elif item[2] == AdditionScores.TRIGGER or item[2] == AdditionScores.TRIGGER_NOT or item[2] == AdditionScores.THEME_ACTION:
            new_result.append((item[1], item[0], item[2]))
        else:
            new_result.append(item)

    return new_result


def checkConditionTheme(item):
    if item == 'khi' or item == 'để' or item == 'bởi':
        return True
    else:
        return False


def checkConditionTarget(item):
    if item == 'được' or item == 'do' or item == 'bị':
        return True
    else:
        return False


def checkConditionType(item):
    if item == 'N' or item == 'Np' or item == 'Nc':
        return True
    else:
        return False


def readd_adverbs(input_query):
    reduced = reduce_words(input_query)
    #print(reduced)
    result = []
    idx = 0
    while idx < len(reduced):
        result.append(reduced[idx])
        if idx + 1 < len(reduced):
            if reduced[idx][1] == 'V' and reduced[idx][1] == 'hưởng':
                result.append(('nhằm', 'AD', AdditionScores.NONE))
            elif reduced[idx][1] == 'V' and reduced[idx+1][1] == 'V':
                result.append(('việc', 'AD', AdditionScores.NONE))
        idx = idx + 1

    return result


def reduce_words(input_query):
    # print("------------------------------------------")
    query = filter_words(pos_tag(handle_in_query(input_query)))
    # print("Gốc:", query)
    skip = 0
    list_query = []
    start = 0
    while start < len(query):
        list_same_names = []
        if skip != 0:
            skip = skip - 1
        else:
            namesList = data.getSameKeywordsList(query[start][0])
            for name in namesList:
                list_same_names.append(name)

            count_inclued = len(list_same_names)
            if(count_inclued != 0):
                max_step = -1
                matched = False
                score = AdditionScores.NONE
                get_data = ""
                for item in list_same_names:
                    step = getChildLength(
                        query[start][0],start, item, query)

                    text = query[start][0]

                    if step > 0:
                        for idx in range(1, step+1):
                            text = text + " " + query[start+idx][0]

                    #print(query[start][0], "---", item[0], "------------------------    Step:", step, "/Max-step:", max_step, "/text:", text)

                    if step > max_step or matched == False:
                        if text == item[0]:
                            max_step = step
                            get_data = text
                            score = item[1]
                            matched = True
                        elif matched == False:
                            max_step = step
                            get_data = item[0]
                            score = item[1]

                skip = max_step if max_step > 0 else 0
                list_query.append(
                    (query[start][0] if max_step == -1 else get_data, 'Np' if max_step > 0 else query[start][1], score))
            else:
                list_query.append(
                    (query[start][0], query[start][1], AdditionScores.NONE))
        start = start + 1

    return list_query


def getChildLength(title, start,data, query):
    wordsList = filter_words(pos_tag(data[0]))
    data_types_included = checkVariableTypesIncluded(wordsList)
    end = -1
    #print("Root:",pos_tag(data[0]),"-Extracted:",wordsList)
    for index in range(0, len(query)):
        if wordsList[-1][0] == query[index][0]:
            end = index
        if end >= start and end != -1:
            break
    #print(start, "///", end, query, wordsList)
    if end == -1 or end - start + 1 > len(wordsList):
        return -1
    else:
        step = -1
        appearedWordsList = []
        for index in range(start, end+1):
            appeared = False
            # print(query[index][0])
            appearedWordsList.append(query[index])
            for it in wordsList:

                if(it[0] == query[index][0]):
                    step = step + 1
                    appeared = True
                #print(it[0], "==+==", query[index][0])
            if appeared == False:
                #print('Case 1')
                return 0
        #print(appearedWordsList, "---", checkVariableTypesIncluded(appearedWordsList),'==', wordsList, "---", data_types_included)
        if checkVariableTypesIncluded(appearedWordsList) == data_types_included or len(appearedWordsList) == len(wordsList):
            #print('Case 2')
            return step
        else:
            #print('Case 3')
            return 0


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


# def define_connection(word_1, word_2):
#     type_of_connection = ""
#     if(word_2[1] == 'V'):
#         for item in data_type:
#             value = item.getConntectorType(word_1[0])
#             if value:
#                 type_of_connection = value
#         if type_of_connection == 'người':
#             return 'tác nhân'
#         else:
#             return 'ngữ cảnh'
#     else:
#         for item in data_type:
#             value = item.getConntectorType(word_2[0])
#             if value:
#                 type_of_connection = value
#         if not type_of_connection:
#             return 'đối tượng'
#         else:
#             return type_of_connection
