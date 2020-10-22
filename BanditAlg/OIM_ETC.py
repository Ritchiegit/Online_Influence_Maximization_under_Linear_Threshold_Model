import numpy as np
class OIM_ETC_Algorithm:
    def __init__(self, G, EwTrue, seedSize, oracle, iterationTime, budgetTime):
        # initiate Algorithms parameters
        self.G = G
        self.EwTrue = EwTrue  # For comparison
        self.seedSize = seedSize
        self.iterationTime = iterationTime  # Total iteration
        self.oracle = oracle
        self.lossList = []
        self.iterCounter = 0  # iteration times

        self.index2Node = []
        for v in self.G.nodes():
            self.index2Node.append(v)

        self.budgetTime = budgetTime
        self.XactivatedCounter = {}
        self.EwHat = {}
        for edge in self.G.in_edges():
            self.XactivatedCounter[edge] = 0
            self.EwHat[edge] = 0


    def decide(self):
        # S = []
        if self.iterCounter < self.budgetTime*self.G.number_of_nodes():
            uToLearning = self.index2Node[self.iterCounter % self.G.number_of_nodes()]
            S = [uToLearning]  # one node as seed set
        else:
            S = self.oracle(self.G, self.EwHat, self.seedSize)
        norm1BetweenEwEstimate_EwTrue = 0
        for u, v in self.EwTrue:
            norm1BetweenEwEstimate_EwTrue = norm1BetweenEwEstimate_EwTrue + abs(self.EwHat[(u, v)] - self.EwTrue[(u, v)])
        print("norm1BetweenEwEstimate_EwTrue", norm1BetweenEwEstimate_EwTrue)
        self.lossList.append(norm1BetweenEwEstimate_EwTrue)
        EwEstimated = self.EwHat
        return S, EwEstimated

    def updateParameters(self, finalInfluencedNodeList, attemptingActivateInNodeDir,
                             ActivateInNodeOfFinalInfluencedNodeListDir_AMomentBefore):

        # update Algorithms parameters
        if self.iterCounter < self.budgetTime*self.G.number_of_nodes():
            uToLearning = self.index2Node[self.iterCounter % self.G.number_of_nodes()]
            # Update all outgoing edges of node u
            for edge in self.G.out_edges(uToLearning):
                v = edge[1]
                if v in finalInfluencedNodeList:
                    # Only when the initial node uToLearning affects v can it be counted in the counter
                    if len(attemptingActivateInNodeDir[v]) == 1:
                        self.XactivatedCounter[edge] += 1

        if self.iterCounter == self.budgetTime*self.G.number_of_nodes()-1:
            for edge in self.G.out_edges():
                self.EwHat[edge] = self.XactivatedCounter[edge] / self.budgetTime

        self.iterCounter += 1

    def getLoss(self):
        return np.asarray(self.lossList)