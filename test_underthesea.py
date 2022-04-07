from operator import truediv
from process_data import reduce_word, handle_synonyms_in_query
from process_graph import generate_edges, generate_graph, create_same_arcs
from process_comparison import conceptual_similarity, relational_similarity, calculate_a
import json

from underthesea import word_tokenize, chunk, pos_tag, ner, classify
from collections import defaultdict

if __name__ == '__main__':
    # while True:
    #query = input("Query Input: ")
    query = "Thủ tục đề nghị hỗ trợ học nghề cần những gì ?"
    query = "Quyền của người sử dụng lao động tham gia bảo hiểm thất nghiệp được quy định như thế nào?"
    query = "Các quy định đóng bảo hiểm thất nghiệp cho người lao động cụ thể ra sao ?"
    query = "Mức hỗ trợ mà người sử dụng lao động được hưởng từ quỹ bảo hiểm thất nghiệp do ảnh hưởng bởi đại dịch COVID-19 ?"

    data_list = []

    # Read list titles of laws
    f = open('data.json', encoding="utf8")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for item in data:
        data_list.append([item['id'], item['title']])

    f.close()

    query_synonym = handle_synonyms_in_query(query)
    query_pos_tag = pos_tag(query_synonym)

    query_reduced = reduce_word(query_pos_tag, True)
    queury_graph = generate_graph(query_reduced)
    queury_graph_arcs = generate_edges(queury_graph)

    print("================================================================")
    print("Query replaced synonyms:", query_synonym)
    print("Converted query reduced:", query_reduced)
    print("----------------------------------------------------------------")
    print("Sc        |     Sr        |     S         |     ID")
    print("======================================================")

    score_table = []

    for item_data in data_list:
        # if(item_data[0] != 35 and item_data[0] != 36):
        #     continue
        g_graph = []
        data_graph = generate_graph(
            reduce_word(pos_tag(item_data[1]), False))

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

        if(Sc != 0):
            Sr = relational_similarity(len(g_graph_arcs), mGcG1, mGcG2)
            a = calculate_a(len(g_graph), mGcG1, mGcG2)
            S = Sc * (a + (1-a)*Sr)
        else:
            Sr = 0
            S = 0

        # print("Data: ", "Arcs: ", g_graph)
        # print("Data: ", "Arcs: ", pos_tag(item_data[1]))
        print('{0:.3f}'.format(Sc), '{0:.3f}'.format(
            Sr), '{0:.3f}'.format(S), item_data[0], sep="     |     ")
        score_table.append(S)

    print("======================================================")
    highest_score_positions = [index for index, item in enumerate(
        score_table) if item == max(score_table)]
    for idx in highest_score_positions:
        print("Matched:", data_list[idx][1])

    print("================================================================")
