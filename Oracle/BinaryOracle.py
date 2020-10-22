def getSpreadOfBinary(G, Eweight, S):
    spread = len(S)
    for seed in S:
        for edge in G.out_edges(seed):
            spread += Eweight[edge]
    return spread

def getOracleOfBinary(G, Eweight, seed_size):
    spreadOfV_Dir = {}
    for node in G.nodes():
        tmpSpread = 0
        for edge in G.out_edges(node):
            tmpSpread += Eweight[edge]
        spreadOfV_Dir[node] = tmpSpread
    sortedNode = sorted(spreadOfV_Dir, key=spreadOfV_Dir.__getitem__, reverse=True)
    S = sortedNode[:seed_size]
    return S
