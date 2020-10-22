import numpy as np
import random
import Oracle.OIM_LT_Oracle


class IMLinUCB_LT_Algorithm:
    def __init__(self, G, EwTrue, seed_size, iterationTime, sigma, delta, IM_oracle, IM_cal_reward,
                 scaleTOrNot=False, scaleCRatio=1, scaleGaussianRatio=1, sampleStrategy="GaussianPrioritySample"):
        # initiate Algorithms parameters
        self.G = G
        self.EwTrue = EwTrue  # For comparison
        self.seed_size = seed_size
        self.iterationTime = iterationTime  # Total iteration
        self.iterCounter = 0  # iteration times

        # self.sigma = sigma
        # self.delta = delta
        self.IM_oracle = IM_oracle
        self.IM_cal_reward = IM_cal_reward
        self.loss_list = []

        self.V = np.eye(G.number_of_edges())
        self.b = np.zeros((G.number_of_edges(), 1))
        self.edge2Index = {}
        index = 0
        for v in self.G.nodes():
            for edge in G.in_edges(v):
                self.edge2Index[edge] = index
                index += 1
        self.scaleTOrNot = scaleTOrNot
        self.scaleCRatio = scaleCRatio
        self.scaleGaussianRatio = scaleGaussianRatio
        self.sampleStrategy = sampleStrategy


    def decide(self):
        m = self.G.number_of_edges()
        n = self.G.number_of_nodes()
        if self.scaleTOrNot == True:
            T = self.iterCounter+1
        else:
            T = self.iterationTime
        c = (np.sqrt(m * np.log(1 + T * n) + 2 * np.log(T*(n+1-self.seed_size))) + np.sqrt(n)) ** 2
        c = c * self.scaleCRatio
        epsilon = 1 / np.sqrt(self.iterationTime)

        S, EwEstimated = Oracle.OIM_LT_Oracle.IMLinUCB_Oracle(self.V, self.b, c, epsilon, self.IM_oracle, self.IM_cal_reward, self.seed_size, self.G, self.edge2Index, sampleStrategy=self.sampleStrategy, scaleGaussianRatio=self.scaleGaussianRatio)

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
            activeEdgeOnehot_v = np.zeros((self.G.number_of_edges(), 1))  # A_u
            if v in finalInfluencedNodeList:
                # finalInfluencedNodeList
                if len(attemptingActivateInNodeDir_AMomentBefore) > 0:
                    # If the activated inedge is not none
                    choice = random.choice((1, 2))
                    if choice == 1:  # with prob 1/2
                        for edge in self.G.in_edges(v):
                            indexOfEdge = self.edge2Index[edge]
                            if edge[0] in attemptingActivateInNodeDir[v]:
                                activeEdgeOnehot_v[indexOfEdge][0] = 1
                        y = 1
                    else:  # with prob 1/2
                        for edge in self.G.in_edges(v):
                            indexOfEdge = self.edge2Index[edge]
                            if edge[0] in attemptingActivateInNodeDir_AMomentBefore[v]:
                                activeEdgeOnehot_v[indexOfEdge][0] = 1
                        y = 0
                else:
                    # If it is none
                    for edge in self.G.in_edges(v):
                        indexOfEdge = self.edge2Index[edge]
                        if edge[0] in attemptingActivateInNodeDir[v]:
                            activeEdgeOnehot_v[indexOfEdge][0] = 1
                        y = 1
            else:
                # not finalInfluencedNodeList
                for edge in self.G.in_edges(v):
                    indexOfEdge = self.edge2Index[edge]
                    if edge[0] in attemptingActivateInNodeDir[v]:
                        activeEdgeOnehot_v[indexOfEdge][0] = 1
                y = 0
            self.V = self.V + activeEdgeOnehot_v.dot(activeEdgeOnehot_v.T)
            self.b = self.b + activeEdgeOnehot_v*y
        self.iterCounter += 1

    def getLoss(self):
        return np.asarray(self.loss_list)