from turtle import pos
from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from process_data import handle_in_query, reduce_word
from query import query_data
from generate_data import data_type

# for item in query_data:
#     print("-------------------------------------------------------", end="\n\n")
#     print(reduce_word(pos_tag(handle_in_query(item))), end="\n\n")

query = reduce_word(pos_tag(handle_in_query(query_data[0])))
for item in query:
    list_same_names = []
    for type in data_type:
        for name in type.getSameNames(item[0]):
            if(name):
                list_same_names.append(name)
    print(item[0], "------", list_same_names)

# list_same_names = []
# for type in data_type:
#     for name in type.getSameNames(query[-1][0]):
#         if(name):
#             list_same_names.append(name)
# print("------", list_same_names)
