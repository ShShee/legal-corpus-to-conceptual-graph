from comparsionHandler import ComparisonHandler
from conceptualGraph import ConceptualGraph
from enums import DataPathTypes
import json

from query_handler import reduce_words


class DataHandler:
    def __init__(self, lawsPath, articlesPath, rulesPath, lookupsPath):
        self.laws = self.__retrieveData(lawsPath)
        self.articles = self.__retrieveData(articlesPath)
        self.rules = self.__retrieveData(rulesPath)
        self.lookups = self.__retrieveData(lookupsPath)

        self.graphs = self.__conceptualizeKeyphrase()

    def __retrieveData(self, path):
        """
        Input: type of data that we need to retrive
        Output: list data in this file
        """
        result = []
        # Read list titles of laws
        f = open(path, encoding="utf8")

        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for item in data:
            result.append(item)

        f.close()
        return result

    def __conceptualizeKeyphrase(self):
        """
        Output: list data about articles and rules converted to conceptual graphs
        """
        result = []
        for article in self.articles:
            keyphrase = article["keyphrase"]
            if keyphrase:
                result.append((ConceptualGraph(reduce_words(keyphrase)),
                              article["id"], DataPathTypes.ARTICLES))

        for rule in self.rules:
            keyphrase = rule["keyphrase"]
            if keyphrase:
                result.append(
                    (ConceptualGraph(reduce_words(keyphrase)), rule["id"], DataPathTypes.RULES))

        return result

    def getData(self, type):
        """
        Input: Enum type of data that we want to get
        Output: list json objects of input type
        """
        if type == DataPathTypes.LAWS:
            return self.laws
        elif type == DataPathTypes.ARTICLES:
            return self.articles
        elif type == DataPathTypes.RULES:
            return self.rules
        elif type == DataPathTypes.LOOKUPS:
            return self.lookups

    def compare(self, graph):
        result = []
        """
        Input: Graph of query that we want to compare
        Output: list of top similarities of this graph to data
        """
        for data in self.graphs:
            #print("------------------------")
            comparisonHandler = ComparisonHandler(graph, data[0])
            result.append((data[1],comparisonHandler.getSimilarityScore()))
            # print("Nodes:", data[0].getNodes(), "- Score of", data[1], "is",comparisonHandler.getSimilarityScore())
        return result

    def print(self):
        print(self.laws)
