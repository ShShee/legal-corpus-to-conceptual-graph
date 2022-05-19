from turtle import pos
from regex import P
from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from comparsionHandler import ComparisonHandler
from dataHandler import DataHandler
from enums import DataPathTypes
from query_handler import handle_in_query, reduce_words, define_connection
from query import query_data
from generate_data import data_type
from conceptualGraph import ConceptualGraph

# test = ConceptualGraph(reduce_words(
#     "Người đang hưởng trợ cấp thất nghiệp có được hưởng chế độ bảo hiểm y tế không?"))
# test2 = ConceptualGraph(reduce_words(
#     "hưởng bảo hiểm hiểm y tế trợ cấp thất nghiệp"))
test3 = "rule/29"
# comparisonHandler = ComparisonHandler(test, test2)
# comparisonHandler.getNodes()
# test3 = ComparisonHandler(test, test2)
# #test.print()
# print(test3.getSimilarityScore())
dir = "./data/"
# dataHandler = DataHandler(
#     dir+"laws.json", dir+"articles.json", dir+"rules.json", dir+"lookups.json")

# for query in query_data:
#     print("_-------------------_")
#     print(reduce_words(query))

define_connection("Người đang hưởng trợ cấp thất nghiệp có được hưởng chế độ bảo hiểm y tế không?")
