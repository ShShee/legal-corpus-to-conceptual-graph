import spacy
nlp = spacy.load('vi_core_news_lg')
query = 'Quy định về thông báo tìm kiếm việc làm trong khi đang hưởng hỗ trợ từ trợ cấp thất nghiệp là như thế nào ?'

info_1 = 'Thông báo về việc tìm kiếm việc làm khi hưởng trợ cấp thất nghiệp'
info_2 = 'Trường hợp được bỏ qua thông báo về việc tìm kiếm việc làm khi hưởng trợ cấp thất nghiệp'
info_3 = 'Quy định tham gia bảo hiểm thất nghiệp cho người lao động'
info_4 = 'Giải quyết hưởng trợ cấp thất nghiệp'
info_5 = 'Thủ tục xin hỗ trợ học nghề'

init_query_list = []
init_data_list = []
init_query_list.append(nlp(query))

init_data_list.append(nlp(info_1))
init_data_list.append(nlp(info_2))
init_data_list.append(nlp(info_3))
init_data_list.append(nlp(info_4))
init_data_list.append(nlp(info_5))

def reduce_word(input_list):
    reduced = []
    for token in input_list:
        if(token.tag_=='N' or token.tag_=='Nc' or token.tag_=='V'):
            reduced.append(token.text)
    return reduced

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


def create_same_arcs(g_graph):
    arcs = []

    for idx in range(len(g_graph)-1):
        if(g_graph[idx][1]+1 == g_graph[idx+1][1]):
            arcs.append((g_graph[idx][0], g_graph[idx+1][0]))

    return arcs


def conceptual_similarity(nGc, nG1, nG2):
    return (2*nGc)/(nG1 + nG2)


def relational_similarity(mGc, mGcG1, mGcG2):
    return (2*mGc)/(mGcG1 + mGcG2)


def calculate_a(nGc, mGcG1, mGcG2):
    return (2*nGc)/(2*nGc+mGcG1 + mGcG2)


for item_query in init_query_list:
    print("======================================================")
    print("Query:", item_query)
    print("------------------------------------------------------")
    print("Sc        |     Sr        |     S")
    print("======================================================")
    queury_graph = generate_graph(reduce_word(item_query))
    queury_graph_arcs = generate_edges(queury_graph)

    for item_data in init_data_list:
        g_graph = []
        data_graph = generate_graph(reduce_word(item_data))

        # Retrieve similar nodes
        for node_index, node_query in enumerate(queury_graph):
            for node_data in data_graph:
                if(node_query.lower() == node_data.lower()):
                    g_graph.append([node_query, node_index])

        # Generate arcs list
        g_graph_arcs = create_same_arcs(g_graph)
        data_graph_arcs = generate_edges(data_graph)
        mGcG1 = len(g_graph_arcs)
        mGcG2 = len(g_graph_arcs)

        # Remove same arcs with g_graph
        arcs_of_query = [
            elem for elem in queury_graph_arcs if elem not in g_graph_arcs]
        arcs_of_data = [
            elem for elem in data_graph_arcs if elem not in g_graph_arcs]

        # Retrive arcs that connect with nodes of g_graph
        for node in g_graph:
            for arc in arcs_of_query:
                if(node[0] == arc[0] or node[0] == arc[1]):
                    mGcG1 += 1
            for arc in arcs_of_data:
                if(node[0] == arc[0] or node[0] == arc[1]):
                    mGcG2 += 1

        Sc = conceptual_similarity(
            len(g_graph), len(queury_graph), len(data_graph))

        Sr = relational_similarity(len(g_graph_arcs), mGcG1, mGcG2)

        a = calculate_a(len(g_graph), mGcG1, mGcG2)

        S = Sc * (a + (1-a)*Sr)

        # print("------------------------------------------------------------------------------------")
        # print("Data: ", "Arcs: ", g_graph)
        # print("Data: ", "Arcs: ", arcs_of_query)
        # print("Data: ", "Arcs: ", arcs_of_data)
        print('{0:.3f}'.format(Sc), '{0:.3f}'.format(Sr), '{0:.3f}'.format(S), sep="     |     ")
        print("------------------------------------------------------")

    print("======================================================")