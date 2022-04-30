def generate_graph(input_list):
    graph = dict.fromkeys(input_list, [])
    for index in range(len(input_list)-1):
        destination_nodes = []
        destination_nodes.append(input_list[index+1])
        graph[input_list[index]] = destination_nodes

    return graph


def generate_edges(graph):
    edges = []

    for node in graph:
        # for each neighbour node of a single node
        for neighbour in graph[node]:
            # if edge exists then append
            edges.append((node, neighbour))

    return edges