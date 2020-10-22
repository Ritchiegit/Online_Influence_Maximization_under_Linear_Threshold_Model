import numpy as np
from itertools import combinations
# get random weight
def getNextRandomWeight(weightLowerBound, weightUpperBound):
    weightNowPos = np.random.uniform(weightLowerBound, weightUpperBound)
    return weightNowPos


### get Best S with DFS - START
def getActivateProbabiltiyByDFS(G, S, Ew, u, visitOneHot, node2Index):
    uActivateProbability = 0
    if u in S:
        return 1
    for parentEdge in G.in_edges(u):
        if visitOneHot[node2Index[parentEdge[0]]] == 0:
            visitOneHot[node2Index[parentEdge[0]]] = 1
            uActivateProbability = uActivateProbability + Ew[parentEdge] * G[parentEdge[0]][parentEdge[1]]['weight'] \
                                   * getActivateProbabiltiyByDFS(G, S, Ew, parentEdge[0], visitOneHot, node2Index)
    return uActivateProbability

def getSpreadSizeByProbability(G, Ew, S):
    node2Index = {}
    index = 0
    for tmp in G.nodes:
        node2Index[tmp] = index
        index += 1
    SpreadSize = len(S)
    for u in G.nodes:
        if u not in S:  # Calculate all nodes that are not seed nodes
            visitOneHot = np.zeros(G.number_of_nodes())
            SpreadSize = SpreadSize + getActivateProbabiltiyByDFS(G, S, Ew, u, visitOneHot, node2Index)
    return SpreadSize

def getDifferentSeedSpread(G, Ew, K):
    BestSpreadSize = 0
    BestSeedSet = []
    for seedCombination in combinations(G.nodes, K):
        tmpSpreadSize = getSpreadSizeByProbability(G, Ew, seedCombination)
        if tmpSpreadSize > BestSpreadSize:
            BestSpreadSize = tmpSpreadSize
            BestSeedSet = list(seedCombination)
    return BestSpreadSize, BestSeedSet

def Enumerate_oracle(G, Ew, K):
    BestSpreadSize, BestSeedSet = getDifferentSeedSpread(G, Ew, K)
    return BestSeedSet
### get Best S with DFS - END
