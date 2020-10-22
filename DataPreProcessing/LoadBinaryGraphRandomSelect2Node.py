import networkx as nx
import matplotlib.pyplot as plt
import random
import pickle
save_graph_dir = '..//Datasets//'
number_of_outNode = 10
number_of_inNode = 10
G = nx.DiGraph()
dir_of_edgeWeight = {}
list_of_triples_of_edge = []  # source, target, weight
outNodeList = []
inNodeList = []
for i in range(1, number_of_outNode+1):
    Name_of_outNode = i * 2 - 1
    outNodeList.append(Name_of_outNode)
for i in range(1, number_of_inNode+1):
    Name_of_inNode = i * 2
    inNodeList.append(Name_of_inNode)
print("outNodeList", outNodeList)
print("inNodeList", inNodeList)
for inNode in inNodeList:
    connectedOutNode = random.sample(outNodeList, 2)
    for eachConnectedOutNode in connectedOutNode:
        list_of_triples_of_edge.append((eachConnectedOutNode, inNode, 1))
        dir_of_edgeWeight[(eachConnectedOutNode, inNode)] = random.uniform(0, 1)

G.add_weighted_edges_from(list_of_triples_of_edge)

for node in G.nodes():
    sum_of_edge_weight_V = 0
    for edge in G.in_edges(node):
        sum_of_edge_weight_V += dir_of_edgeWeight[edge]
    if sum_of_edge_weight_V > 1+1e-4:
        for edge in G.in_edges(node):
            dir_of_edgeWeight[edge] = dir_of_edgeWeight[edge]/sum_of_edge_weight_V

EwTrue = dir_of_edgeWeight
print(G.nodes)

print(G.in_edges)
print(G.number_of_nodes())
print(G.number_of_edges())
print("edge Raw Weight")
print("EwTrue", EwTrue)
pickle.dump(G, open(save_graph_dir + 'DIY_Binary_RandomSelect2_'+ str(number_of_outNode)+"_"+ str(number_of_inNode)+'.G', "wb"))
pickle.dump(EwTrue, open(save_graph_dir + 'DIY_Binary_RandomSelect2_'+ str(number_of_outNode)+"_"+ str(number_of_inNode)+'EWTrue.dic', "wb"))
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
