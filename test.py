from turtle import pos
from regex import P
from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from query_handler import reduce_words
from query import query_data
from generate_data import data_type

reduce_words(query_data)
