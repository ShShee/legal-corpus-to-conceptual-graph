from turtle import pos
from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from process_data import handle_in_query, reduce_word
from query import query_data
from generate_data import data_type

# for item in query_data:
#     print("-------------------------------------------------------", end="\n\n")
#     print(reduce_word(pos_tag(handle_in_query(item))), end="\n\n")

query = reduce_word(pos_tag(handle_in_query(query_data[0])))
skip = 0
words = []
list_query = []
for item in query:
    list_same_names = []
    if skip == 0:
        words = [item[0]]
    else:
        words.append(item[0])
        skip = skip - 1

    for type in data_type:
        for name in type.getSameNames(' '.join(words)):
            if(name):
                list_same_names.append(name)

    count_inclued = len(list_same_names)
    if(count_inclued == 0):
        for word in words:
            list_query.append(word)
    elif (count_inclued == 1 and ' '.join(words) == list_same_names[0]):
        list_query.append(' '.join(words))
    else:
        skip = skip+1

print(list_query)
# list_same_names = []
# for type in data_type:
#     for name in type.getSameNames(query[-1][0]):
#         if(name):
#             list_same_names.append(name)
# print("------", list_same_names)
