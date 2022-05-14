from ast import keyword
import networkx as nx

from conceptualGraph import ConceptualGraph
from enums import DataPathTypes, AdditionScores, additionScoring


class ComparisonHandler(ConceptualGraph):
    def __init__(self, graph_1, graph_2):
        """
        Input: graph_1 and graph_2 for initialization of same graph between them
        """
        self.graph = nx.Graph()

        same_nodes = graph_2.getSameNodes(graph_1)
        self.graph.add_nodes_from(same_nodes)

        # Size of nodes in graph
        self.nGcs = self.countNodes()
        self.nG1s = graph_1.countNodes()
        self.nG2s = graph_2.countNodes()

        # Size of same edges in comparison with this graph
        if len(same_nodes) != 0:
            self.__addEdgeWithWeight(
                graph_2.getEdgesFromGivenNodes(same_nodes))
            sameEdges = self.__getSameEdges(graph_1)

            self.graph.clear()
            self.graph.add_nodes_from(same_nodes)
            self.__addEdgeWithWeight(sameEdges)

            self.mGc = self.countEdgesWithWeights()
            self.mGcG1 = self.countEdgesWithWeights(graph_1)
            self.mGcG2 = self.countEdgesWithWeights(graph_2)
        else:
            self.mGc = 0
            self.mGcG1 = 0
            self.mGcG2 = 0

    def __addEdgeWithWeight(self, result):
        edges, weights = result

        for idx, value in enumerate(edges):
            self.graph.add_edge(value[0], value[1], weight=weights[idx])

    def __compare2Edges(self, graph, edge_1, edge_2):
        #print(self.get_edge_attributes("weight"))
        weight = self.get_edge_attributes(
            "weight")[edge_1] == graph.get_edge_attributes("weight")[edge_2]
        if weight:
            if ((edge_2[0][0] == edge_1[0][0] and edge_2[1][0] == edge_1[1][0]) or (edge_2[0][0] == edge_1[1][0] and edge_2[1][0] == edge_1[0][0])):
                return True
        else:
            return False

    def __getSameEdges(self, graph):
        result = []
        weights = []
        for edge in self.getEdges():
            for edge_compare in graph.getEdges():
                if self.__compare2Edges(graph, edge, edge_compare):
                    result.append(edge)
                    weights.append(self.get_edge_attributes("weight")[edge])
        return (result, weights)

    def conceptual_similarity(self):
        return (2*self.nGcs)/(self.nG1s + self.nG2s)

    def relational_similarity(self):
        #print("1: ",self.mGcG1,"--- 2: ",self.mGcG2, "--- same:",self.mGc)
        denominator = self.mGcG1 + self.mGcG2
        return (2*self.mGc)/denominator if denominator != 0 else 0

    def __calculate_a(self):
        denominator = 2*self.nGcs + self.mGcG1 + self.mGcG2
        return (2*self.nGcs)/denominator if denominator != 0 else 0

    def getSimilarityScore(self, dataType):
        addition_type_score = additionScoring(AdditionScores.IS_ARTICLE) if dataType == DataPathTypes.ARTICLES else 0
        similariy_score = self.conceptual_similarity() * (self.__calculate_a() +
                                                            (1 - self.__calculate_a()) * self.relational_similarity())

        total = round(similariy_score +
                      addition_type_score if similariy_score != 0 else 0, 5)
        return total
