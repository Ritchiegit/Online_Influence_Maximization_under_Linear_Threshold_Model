import numpy as np
import random
import Oracle.OIM_LT_Oracle_for_little_V_binary_2d


class IMLinUCB_LT_Algorithm:
    def __init__(self, G, EwTrue, seed_size, iterationTime, sigma, delta, IM_oracle, IM_cal_reward,
                 scaleTOrNot=False, scaleCRatio=1, scaleGaussianRatio=1, sampleStrategy="2d"):
        # initiate Algorithms parameters
        self.G = G
        self.EwTrue = EwTrue  # For comparison
        self.seed_size = seed_size
        self.iterationTime = iterationTime  # Total iteration
        self.iterCounter = 0  # iteration times
        # self.sigma = sigma
        self.delta = delta
        self.loss_list = []
        # For each node there is a V b
        # edge2index
        self.VDir = {}
        self.bDir = {}
        self.edge2IndexDir = {}
        for v in self.G.nodes:
            self.VDir[v] = np.eye(G.in_degree[v])
            self.bDir[v] = np.zeros((G.in_degree[v], 1))
            self.edge2IndexDir[v] = {}
            index = 0
            for edge in G.in_edges(v):
                self.edge2IndexDir[v][edge] = index
                index += 1

        self.scaleTOrNot = scaleTOrNot
        self.scaleCRatio = scaleCRatio

    def decide(self):
        if self.scaleTOrNot == True:
            T = self.iterCounter + 1
        else:
            T = self.iterationTime
        cDir = {}
        for v in self.G.nodes():
            cDir[v] = (np.sqrt(self.G.in_degree[v] * np.log(1 + T) + 2 * np.log(1 / self.delta)) + np.sqrt(self.G.in_degree[v])) ** 2
            cDir[v] = cDir[v] * self.scaleCRatio

        S, EwEstimated, spread = Oracle.OIM_LT_Oracle_for_little_V_binary_2d.IMLinUCB_Oracle(self.VDir, self.bDir, cDir, self.seed_size, self.G, self.edge2IndexDir)

        norm1BetweenEwEstimate_EwTrue = 0
        for u, v in self.EwTrue:
            norm1BetweenEwEstimate_EwTrue = norm1BetweenEwEstimate_EwTrue + abs(EwEstimated[(u, v)] - self.EwTrue[(u, v)])*self.G[u][v]['weight']
        print("norm1BetweenEwEstimate_EwTrue", norm1BetweenEwEstimate_EwTrue)
        self.loss_list.append(norm1BetweenEwEstimate_EwTrue)
        return S, EwEstimated

    def updateParameters(self, finalInfluencedNodeList, attemptingActivateInNodeDir,
                         attemptingActivateInNodeDir_AMomentBefore):
        # update Algorithms parameters

        # finalInfluencedNodeList: The nodes activated after spreading.
        # attemptingActivateInNodeDir:
        #   1. For the nodes activated: The activation of the incoming edge at the moment of the activated node is activated
        #   2. For the nodes not activated after spreading: The activation of the incoming edge after the end
        # attemptingActivateInNodeDir_AMomentBefore: The activation of the incoming edge just before the moment of the activated node is activated

        # Update every edge observed
        for v in self.G.nodes():
            activeEdgeOnehot_v = np.zeros((self.G.in_degree[v], 1))
            # finalInfluencedNodeList
            if v in finalInfluencedNodeList:
                if len(attemptingActivateInNodeDir_AMomentBefore) > 0:
                    # If the activated inedge is not none
                    choice = random.choice((1, 2))
                    if choice == 1:  # with prob 1/2
                        for edge in self.G.in_edges(v):
                            indexOfEdge = self.edge2IndexDir[v][edge]
                            if edge[0] in attemptingActivateInNodeDir[v]:
                                activeEdgeOnehot_v[indexOfEdge][0] = 1
                        y = 1
                    else:  # with prob 1/2
                        for edge in self.G.in_edges(v):
                            indexOfEdge = self.edge2IndexDir[v][edge]
                            if edge[0] in attemptingActivateInNodeDir_AMomentBefore[v]:
                                activeEdgeOnehot_v[indexOfEdge][0] = 1
                        y = 0
                else:
                    # If it is none
                    for edge in self.G.in_edges(v):
                        indexOfEdge = self.edge2IndexDir[v][edge]
                        if edge[0] in attemptingActivateInNodeDir[v]:
                            activeEdgeOnehot_v[indexOfEdge][0] = 1
                        y = 1
            else:
                # not finalInfluencedNodeList
                for edge in self.G.in_edges(v):
                    indexOfEdge = self.edge2IndexDir[v][edge]
                    if edge[0] in attemptingActivateInNodeDir[v]:
                        activeEdgeOnehot_v[indexOfEdge][0] = 1
                y = 0
            self.VDir[v] = self.VDir[v] + activeEdgeOnehot_v.dot(activeEdgeOnehot_v.T)
            self.bDir[v] = self.bDir[v] + activeEdgeOnehot_v * y
        self.iterCounter += 1

    def getLoss(self):
        return np.asarray(self.loss_list)