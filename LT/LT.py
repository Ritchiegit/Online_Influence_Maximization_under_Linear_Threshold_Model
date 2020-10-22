import random
from copy import deepcopy
import networkx as nx

def uniformWeights(G):
    '''
    Every incoming edge of v with degree dv has weight 1/dv.
    '''
    Ew = dict()
    for u in G:
        in_edges = G.in_edges([u], data=True)
        dv = sum([edata['weight'] for v1,v2,edata in in_edges])
        for v1,v2,_ in in_edges:
            Ew[(v1,v2)] = 1/dv
    return Ew


def randomWeights(G):
    '''
    Every edge has random weight.
    After weights assigned,
    we normalize weights of all incoming edges so that they sum to 1.
    '''
    Ew = dict()
    for u in G:
        in_edges = G.in_edges([u], data=True)
        ew = [random.random() for e in in_edges]  # random edge weights
        total = 0  # total sum of weights of incoming edges (for normalization)
        for num, (v1, v2, edata) in enumerate(in_edges):
            total += edata['weight']*ew[num]
        if total > 1:
            for num, (v1, v2, _) in enumerate(in_edges):
                Ew[(v1, v2)] = ew[num]/total
        else:
            for num, (v1, v2, _) in enumerate(in_edges):
                Ew[(v1, v2)] = ew[num]

    return Ew

def checkLT(G, Ew, eps = 1e-4):
    for u in G:
        in_edges = G.in_edges([u], data=True)
        total = 0
        for (v1, v2, edata) in in_edges:
            total += Ew[(v1, v2)]*G[v1][v2]['weight']
        if total >= 1 + eps:
            return 'For node %s LT property is incorrect. Sum equals to %s' %(u, total)
    return True

def runLT(G, S, Ew):
    '''
    Input: G -- networkx directed graph
    S -- initial seed set of nodes
    Ew -- influence weights of edges
    NOTE: multiple k edges between nodes (u,v) are
    considered as one node with weight k. For this reason
    when u is activated the total weight of (u,v) = Ew[(u,v)]*k
    '''

    assert type(G) == nx.DiGraph, 'Graph G should be an instance of networkx.DiGraph'
    assert type(S) == list, 'Seed set S should be an instance of list'
    assert type(Ew) == dict, 'Infleunce edge weights Ew should be an instance of dict'

    T = deepcopy(S)  # targeted set
    lv = dict()  # threshold for nodes
    for u in G:
        lv[u] = random.random()
    W = dict(zip(G.nodes(), [0]*len(G)))  # weighted number of activated in-neighbors

    Sj = deepcopy(S)  # For Extension
    while len(Sj):  # while we have newly activated nodes
        Snew = []
        for u in Sj:
            for v in G[u]:  # In G，Sj u's out edge to v。
                if v not in T:
                    W[v] += Ew[(u,v)]*G[u][v]['weight']
                    if W[v] >= lv[v]:  # if greater than threshold
                        Snew.append(v)
                        T.append(v)
        Sj = deepcopy(Snew)

    return T

def runLT_NodeFeedback(G, S, Ew):
    '''
    Input: G -- networkx directed graph
    S -- initial seed set of nodes
    Ew -- influence weights of edges
    NOTE: multiple k edges between nodes (u,v) are
    considered as one node with weight k. For this reason
    when u is activated the total weight of (u,v) = Ew[(u,v)]*k
    '''

    assert type(G) == nx.DiGraph, 'Graph G should be an instance of networkx.DiGraph'
    assert type(S) == list, 'Seed set S should be an instance of list'
    assert type(Ew) == dict, 'Infleunce edge weights Ew should be an instance of dict'
    # attemptingActivateInNodeDir: Maintain a set of ingress nodes to activate for each node
    # workedInNodeList: When the node is activated, it will not continue to accumulate, and will be added to the list matching T
    # key, node, value: List of activated ingress points
    # When accessing u in Sj, add to the list of all inactive nodes v
    attemptingActivateInNodeDir = {}  #
    workedInNodeList = {}
    ActivateInNodeOfFinalInfluencedNodeListDir_AMomentBefore = {}  # The node that is finally activated is in here. With the in edge of the activation at the previous moment。
    for u in S:
        ActivateInNodeOfFinalInfluencedNodeListDir_AMomentBefore[u] = []  # The previous activation of all seed nodes

    T = deepcopy(S)  # targeted set: The node that is finally activated
    lv = dict()  # threshold for nodes
    for u in G:
        lv[u] = random.random()
        attemptingActivateInNodeDir[u] = []

    W = dict(zip(G.nodes(), [0]*len(G)))  # weighted number of activated in-neighbors

    Sj = deepcopy(S)
    # print 'Initial set', Sj
    while len(Sj):
        # Each cycle is a spread
        # print("Sj", Sj)
        Snew = []

        attemptingActivateInNodeDir_AMomentBefore = deepcopy(attemptingActivateInNodeDir)
        for u in Sj:  # For the newly activated node u, mark all its child nodes
            for v in G[u]:  # In the directed graph G, all outgoing edges v of u in Sj.
                if v not in T:  # For v that has not been activated before
                    # Add u to the list of nodes that intend to activate v
                    # (because only v not in T, nodes that are not activated are counted, all counts until they are activated)

                    attemptingActivateInNodeDir[v].append(u)

                    W[v] += Ew[(u, v)] * G[u][v]['weight']
                    if W[v] >= lv[v]:
                        Snew.append(v)
                        T.append(v)
                        workedInNodeList[v] = attemptingActivateInNodeDir[v]  # Record the node that successfully activated v
                        # When activating, record the node activated at the previous moment.
                        ActivateInNodeOfFinalInfluencedNodeListDir_AMomentBefore[v] = deepcopy(attemptingActivateInNodeDir_AMomentBefore[v])
        Sj = deepcopy(Snew)
    reward = len(T)
    return reward, T, workedInNodeList, attemptingActivateInNodeDir, ActivateInNodeOfFinalInfluencedNodeListDir_AMomentBefore

def avgLT(G, S, Ew, iterations):
    avgSize = 0
    progress = 1
    for i in range(iterations):
        if i == round(iterations*.1*progress) - 1:
            progress += 1
        T = runLT(G, S, Ew)
        avgSize += len(T)/iterations  # average diffusion results
    return avgSize