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

define_connection("Thời gian hưởng hỗ trợ học nghề khi tham gia bảo hiểm thất nghiệp được quy định như thế nào?")
# class Phanso:
#     def __init__(self,tu_so,mau_so):
#         self.tu = tu_so
#         self.mau = mau_so

#     def __add__(self,other):
#         return Phanso(self.tu + other.tu,self.mau + other.mau)

#     def __lt__(self,other):
#         print(self.tu,other.tu)
#         return self.tu > other.tu
    
#     def __invert__(self):
#         return Phanso(self.mau,self.tu)
    
#     def printt(self):
#         print(str(self.tu) + "/" + str(self.mau))
    
# a = Phanso(3,5)
# b = Phanso (6,5)
# c = ~b
# c.printt()
