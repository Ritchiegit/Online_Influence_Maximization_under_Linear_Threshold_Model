import igraph
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import random
nodesNum = 12
p = 0.20
save_graph_dir = '..//Datasets//'

def gen_ER_random(nodesNum, p):

    # Generate Graph
    G_raw = igraph.Graph.Erdos_Renyi(n=nodesNum, p=p, directed=True)  # from igraph
    G = nx.DiGraph()

    for edge in G_raw.es:
        G.add_weighted_edges_from([(edge.source, edge.target, 1)])
    return G

G = gen_ER_random(nodesNum=nodesNum, p=p)

dir_of_edgeWeight = {}
for node in G.nodes():
    for edge in G.in_edges(node):
        dir_of_edgeWeight[edge] = random.uniform(0, 1)

for node in G.nodes():
    sum_of_edge_weight_V = 0
    for edge in G.in_edges(node):
        sum_of_edge_weight_V += dir_of_edgeWeight[edge]
    if sum_of_edge_weight_V > 1+1e-4:
        for edge in G.in_edges(node):
            dir_of_edgeWeight[edge] = dir_of_edgeWeight[edge]/sum_of_edge_weight_V

EwTrue = dir_of_edgeWeight

print(G.number_of_nodes())
print(G.number_of_edges())

print(EwTrue)
pickle.dump(G, open(save_graph_dir + "ER_node" + str(nodesNum) + "_p_" + str(p) + '.G', "wb"))
pickle.dump(EwTrue, open(save_graph_dir + "ER_node" + str(nodesNum) + "_p_" + str(p) +'EWTrue.dic', "wb"))
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
