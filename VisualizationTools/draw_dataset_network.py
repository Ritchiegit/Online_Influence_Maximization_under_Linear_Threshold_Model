import matplotlib.pyplot as plt
import networkx as nx
import pickle
import matplotlib
from numpy import array
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

Title = "(e)"
layout = {1: array([0.3776727, 0.48327669]), 0: array([0.44758942, 0.02787252]), 2: array([-0.00109134, -0.25555363]), 3: array([0.35288611, -0.72164935]), 7: array([0.28127489, 0.17933682]), 8: array([-0.3,  0.04827666]), 6: array([0.10805103,  0.19061716]), 4: array([-0.14694817, -0.6042009]), 5: array([-0.00333258,  0.45202404])}
G = pickle.load(open("../Datasets/ER_node9_p_0.2.G", 'rb'), encoding='latin1')
EwTrue = pickle.load(open("../Datasets/ER_node9_p_0.2EWTrue.dic", 'rb'), encoding='latin1')

"""
Title = "(f)"
layout = {11: array([-0.30553974,  0.3042497 ]), 0: array([-0.59247395, -0.11011073]), 1: array([0.36208325, 0.20757496]), 2: array([0.6, 0.22248644]), 7: array([ 0.52543716, -0.24525052]), 4: array([-0.31563801, -0.30050789]), 3: array([ 0.24526581, -0.14482196]), 6: array([-0.29384363, 0.068774]), 5: array([-0.107892 , -0.1095702]), 8: array([-0.15552591,  0.21238039]), 9: array([-0.73217495,  0.1656556 ]), 10: array([0.37030197, 0.04660194])}
G = pickle.load(open("../Datasets/ER_node12_p_0.2.G", 'rb'), encoding='latin1')
EwTrue = pickle.load(open("../Datasets/ER_node12_p_0.2EWTrue.dic", 'rb'), encoding='latin1')
"""

node_label = {}
edge_labels = {}
for key in EwTrue:
    edge_labels[key] = str(round(EwTrue[key], 3))

for node in G.nodes():
    node_label[node] = node
nx.draw_networkx_nodes(G, pos=layout, node_color='grey')
nx.draw_networkx_edges(G, pos=layout)
nx.draw_networkx_labels(G, pos=layout, labels=node_label)
nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels,font_size=5)
plt.title(Title)
plt.show()
