from turtle import pos
from regex import P
from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from query_handler import reduce_words
from query import query_data
from generate_data import data_type

reduce_words(query_data)
# for index in range(0, len(list_query)-1):
#     print(list_query[index][0], "-", list_query[index+1][0],
#           '- Connector:', define_connection(list_query[index], list_query[index+1]))
