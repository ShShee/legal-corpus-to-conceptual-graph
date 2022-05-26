from ast import keyword
import networkx as nx

from conceptualGraph import ConceptualGraph
from enums import DataPathTypes, AdditionScores, additionScoring


class ComparisonHandler(ConceptualGraph):
    def __init__(self, graph_1, graph_2):
        """
        Input: graph_1 and graph_2 for initialization of same graph between them
        """
        self.graph = nx.DiGraph()

        same_nodes = graph_2.getSameNodes(graph_1)
        self.graph.add_nodes_from(same_nodes)

        # Size of nodes in graph
        self.nGcs = self.countNodesWithWeights(graph_1)
        self.nG1s = graph_1.countNodesWithWeights()
        self.nG2s = graph_2.countNodesWithWeights()

        # Size of same edges in comparison with this graph
        if len(same_nodes) != 0:
            #add all edges from graph 2
            self.__addEdgeWithWeight(
                graph_2.getEdgesFromGivenNodes(same_nodes))
            
            #find same edges from graph 2 to graph 1
            sameEdges = self.__getSameEdges(graph_1)

            #clear previous edges then add same edges
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
        edges, weightTypes = result

        for idx, value in enumerate(edges):
            self.graph.add_edge(value[0], value[1], weight=weightTypes[idx])

    def __compare2Edges(self, graph, edge_1, edge_2):
        edge_1_type = self.get_edge_attributes("weight")[edge_1]
        edge_2_type = graph.get_edge_attributes("weight")[edge_2]
        weightType = (edge_1_type == edge_2_type) or (AdditionScores(edge_1_type) == AdditionScores.INTENT and AdditionScores(edge_2_type) == AdditionScores.INTENT_EXTRA)
        if weightType:
            if ((edge_2[0][0] == edge_1[0][0] and edge_2[1][0] == edge_1[1][0]) or (edge_2[0][0] == edge_1[1][0] and edge_2[1][0] == edge_1[0][0])):
                return True
        else:
            return False

    def __getSameEdges(self, graph):
        result = []
        weightTypes = []
        for edge in self.getEdges():
            for edge_compare in graph.getEdges():
                if self.__compare2Edges(graph, edge, edge_compare):
                    result.append(edge)
                    weightTypes.append(self.get_edge_attributes("weight")[edge])
        return (result, weightTypes)

    def conceptual_similarity(self):
        return (2*self.nGcs)/(self.nG1s + self.nG2s)

    def relational_similarity(self):
        denominator = self.mGcG1 + self.mGcG2
        return (2*self.mGc)/denominator if denominator != 0 else 0

    def calculate_a(self):
        denominator = 2*self.nGcs + self.mGcG1 + self.mGcG2
        return (2*self.nGcs)/denominator if denominator != 0 else 0

    def getSimilarityScore(self, dataType):
        addition_type_score = additionScoring(
            AdditionScores.IS_ARTICLE) if dataType == DataPathTypes.ARTICLES else 0
        similariy_score = self.conceptual_similarity() * (self.calculate_a() +
                                                          (1 - self.calculate_a()) * self.relational_similarity())

        total = round(similariy_score +
                      addition_type_score if similariy_score != 0 else 0, 5)
        return total
