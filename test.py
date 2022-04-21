from turtle import pos
from regex import P
from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from process_data import handle_in_query, reduce_word, define_connection
from query import query_data
from generate_data import data_type

for item in query_data:
#print("-------------------------------------------------------", end="\n\n")
# print(reduce_word(pos_tag(handle_in_query(item))), end="\n\n")

    query = reduce_word(pos_tag(handle_in_query(item)))
    skip = 0
    words = []
    pos_list = []
    list_query = []
    start = 0
    last_checkpoint = ""
    while start < len(query):
        list_same_names = []
        start_next = False
        while start_next == False:
            if skip == 0:
                words = [query[start][0]]
                pos_list = [query[start][1]]
            else:
                words.append(query[start][0])
                pos_list.append(query[start][1])
                skip = skip - 1
            for type in data_type:
                for name in type.getSameNames(' '.join(words)):
                    if(name):
                        list_same_names.append(name)

            count_inclued = len(list_same_names)
            if(count_inclued == 0):
                if last_checkpoint:
                    list_query.append((last_checkpoint, 'Np'))
                    last_checkpoint = ""
                else:
                    list_query.append((words[0], pos_list[0]))
                    start = start - len(words) + 2
                    start_next = True
            elif (count_inclued == 1 and ' '.join(words) == list_same_names[0]):
                last_checkpoint = ""
                list_query.append((' '.join(words), 'Np'))
                start = start + 1
                start_next = True
                # else:
                #     list_query.append((list_same_names[0], 'Np'))
            else:
                for name in list_same_names:
                    if(name == ' '.join(words)):
                        last_checkpoint = ' '.join(words)
                start_next = True
                start = start + 1
                skip = skip+1

    print(list_query)
# list_same_names = []
# for type in data_type:
#     for name in type.getSameNames(query[-1][0]):
#         if(name):
#             list_same_names.append(name)
# print("------", list_same_names)

# for index in range(0, len(list_query)-1):
#     print(list_query[index][0], "-", list_query[index+1][0],
#           '- Connector:', define_connection(list_query[index], list_query[index+1]))
