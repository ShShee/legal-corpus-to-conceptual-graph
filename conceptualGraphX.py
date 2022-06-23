import networkx as nx

from query_handler import define_connection, reduce_words
from enums import AdditionScores, additionScoring


class ConceptualGraph:
    def __init__(self, keywords):
        """
        Input: List of keywords to init graph
        """
        self.graph = nx.DiGraph()

        # Old way
        reduced = reduce_words(keywords)

        # New way
        remove_advs = []
        for word in reduced:
            if word[1] != 'AD':
                remove_advs.append(word)

        self.graph.add_nodes_from(remove_advs)
        self._create_edges(remove_advs)

    def _create_edges(self, keywords):
        """
        Input: List of keywords to init edges
        Output: Edges that is connected between 2 adjoined keywords
        """
        for idx in range(len(keywords)-1):
            self.graph.add_edge(keywords[idx], keywords[idx+1], weight=0)
            
    def getGraph(self):
        return self.graph

    def getNodes(self):
        """
        Output: Nodes of this graph
        """
        return self.graph.nodes

    def getEdges(self):
        """
        Output: Edges of this graphs
        """
        return self.graph.edges

    def print(self):
        print("Nodes:", self.graph.nodes)
        print("Edges:", self.graph.edges)

    def getSameNodes(self, graph):
        """
        Input: Graph that needs to be found same nodes with this graph
        Output: List of nodes that appear in both graphs
        """
        result = []
        for item in self.getNodes():
            for node in graph.getNodes():
                if item[0] == node[0]:
                    result.append(node)
                    break
        return result

    def get_edge_attributes(self, name):
        edges = self.graph.edges(data=True)
        return dict((x[:-1], x[-1][name]) for x in edges if name in x[-1])

    def getEdgesFromGivenNodes(self, nodes):
        """
        Turn fullEdge flag on to get edge that connects 2 of nodes in given list
        """
        result = []
        weightTypes = []
        for edge in self.getEdges():
            start_node = list(filter(lambda node: node == edge[0], nodes))
            end_node = list(filter(lambda node: node == edge[1], nodes))

            if start_node and end_node:
                result.append(edge)
                weightTypes.append(self.get_edge_attributes("weight")[edge])

        return (result, weightTypes)

    def __getEdgeFromNodes(self, start_node, end_node):
        return list(filter(lambda edge: start_node == edge[0] and end_node == edge[1], self.getEdges()))

    def getEdgesFromGivenGraph(self, graph):
        """
        Turn fullEdge flag on to get edge that connects 2 of nodes in given list
        """
        result = []
        weights = []
        for edge in graph.getEdges():
            start_node = list(
                filter(lambda node: node == edge[0], self.getNodes()))
            end_node = list(filter(lambda node: node ==
                            edge[1], self.getNodes()))

            if start_node or end_node:
                result.append(edge)
                weight = additionScoring(AdditionScores(
                    graph.get_edge_attributes("weight")[edge]))
                weights.append(0 if start_node and end_node and self.__getEdgeFromNodes(
                    start_node, end_node) else - weight)

        return (result, weights)

    def countEdgesWithWeights(self, graph=None):
        total = 0

        if graph is not None:
            edges, weights = self.getEdgesFromGivenGraph(graph)

            for idx, val in enumerate(edges):
                total = total + 1
        else:
            for idx, val in enumerate(self.getEdges()):
                total = total + 1

        return total

    def countNodesWithWeights(self, graph=None):
        """
        Output: Number of nodes in this graph with weights (every nodes has different score)
        """
        count = 0

        for node in self.graph.nodes:
            count = count + 1
        return count
