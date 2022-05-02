from scipy.fftpack import idct
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
            # print("------------------------")
            comparisonHandler = ComparisonHandler(graph, data[0])
            add_value = (
                # Id of this type of data
                data[1],
                # get title of this data,
                self.getArticleTitle(data[1], data[2]),
                # get index of this rule in article
                self.getRuleTitle(
                    data[1], True) if data[2] == DataPathTypes.RULES else "",
                # get law code of this data,
                ', '.join(self.getCodeList(data[1], data[2])),
                # Get comparison score
                str(comparisonHandler.getSimilarityScore(data[2])),
                # get nodes of data graph
                str(data[0].getNodes()),
                # get nodes of same graph,
                str(comparisonHandler.getNodes())
            )
            result.append(add_value)
            # print("Nodes:", data[0].getNodes(), "- Score of", data[1], "is",comparisonHandler.getSimilarityScore())
        return result

    def getDataFromId(self, id, type):
        return list(filter(lambda val: val["id"] == id, self.articles if type ==
                           DataPathTypes.ARTICLES else self.rules))[0]

    def getLookUpFromId(self, id, type):
        lookUpId = self.getDataFromId(id, type)["lookUpId"]
        return list(filter(lambda lk: lk["id"] == lookUpId, self.lookups))[0]

    def getArticleTitle(self, id, dataType):
        """
        Input: id and type of rule or article
        Output: string title of this article 
        """
        if dataType == DataPathTypes.ARTICLES:
            return self.getDataFromId(id, DataPathTypes.ARTICLES)["title"]
        elif dataType == DataPathTypes.RULES:
            return self.getRuleTitle(id, False)

    def getRuleTitle(self, id, onlyIndex):
        """
        Input: id and type of rule and if we only want to get index of this rule in article turn onlyIndex to True
        Output: string title of the parent article of this rule 
        """
        lookUp = self.getLookUpFromId(id, DataPathTypes.RULES)

        if(onlyIndex):
            indexInArticle = [idx for idx, val in enumerate(
                lookUp["rules"]) if val == id][0]
            return "Khoản "+str(indexInArticle + 1)
        else:
            return self.getArticleTitle(lookUp["article"], DataPathTypes.ARTICLES)

    def getLawFromCode(self, code):
        return list(filter(lambda law: law["code"] == code, self.laws))[0]

    def getArticleFromRule(self, id):
        lookUp = self.getLookUpFromId(id, DataPathTypes.RULES)
        return self.getDataFromId(lookUp["article"], DataPathTypes.ARTICLES)

    def getCodeList(self, id, type):
        return self.getDataFromId(id, type)['laws'] if type == DataPathTypes.ARTICLES else self.getArticleFromRule(id)['laws']

    def getLawTitlesFromList(self, id, type):
        result = []
        for code in self.getCodeList(id, type):
            result.append(self.getLawFromCode(code)['title'])
        return result

    def print(self):
        print(self.laws)
