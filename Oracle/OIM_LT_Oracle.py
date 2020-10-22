import copy
import random
import numpy as np


# get Weigh one by one
def getNextWeight(weightNowPos, initWeight, weightUpperBound, sideLength):
    traverseEnd = 0
    for indexOfWeight in range(len(weightNowPos) + 1):
        if indexOfWeight == len(weightNowPos):
            traverseEnd = 1
            break
        if weightNowPos[indexOfWeight] + sideLength > weightUpperBound[indexOfWeight]:
            continue
        else:
            weightNowPos[indexOfWeight] = weightNowPos[indexOfWeight] + sideLength
            for underIndex in range(indexOfWeight):
                weightNowPos[underIndex] = initWeight[underIndex]
            break
    return weightNowPos, traverseEnd

# get random weight
def getNextRandomWeight(weightLowerBound, weightUpperBound):
    weightNowPos = np.random.uniform(weightLowerBound, weightUpperBound)
    return weightNowPos

def IMLinUCB_Oracle(V, b, c, epsilon, IM_oracle, IM_cal_reward, K, G, edge2Index, sampleStrategy = "RandomGenerate", scaleGaussianRatio=1):
    sideLength = (2 / np.sqrt(3)) * epsilon
    invV = np.linalg.inv(V)
    invVb = invV.dot(b)
    weightLowerBound = np.zeros(b.shape)
    weightUpperBound = np.ones(b.shape)

    initWeight = weightLowerBound + sideLength / 2  # init center
    weightNowPos = copy.deepcopy(initWeight)

    BestS = []
    BestReward = -1
    BestEwEstimated = {}

    i = 0
    indexOfGaussianPrioritySample = 0
    while True:
        if sampleStrategy == "RandomGenerate":
            # print("RandomGenerate")
            cToJudge = c
            sampleSize = 100
            weightNowPos = getNextRandomWeight(weightLowerBound, weightUpperBound)
            if i == sampleSize:
                break
        elif sampleStrategy == "RatioSample":
            cToJudge = c
            weightNowPos, traverseEnd = getNextWeight(weightNowPos, initWeight, weightUpperBound, sideLength)
            if traverseEnd == True:
                break
            sampleRatio = 10
            choiceAns = random.choice(range(sampleRatio))
            if choiceAns == 0:
                continue
        elif sampleStrategy == "GaussianPrioritySample":
            cToJudge = c
            weightAveragePos = invVb
            correlation = invV*scaleGaussianRatio
            weightNowPos = np.random.multivariate_normal(weightAveragePos.flatten(), correlation).reshape(weightAveragePos.shape)
            weightNowPos = weightNowPos.clip(0, 1)
            sampleSize = 10
            if indexOfGaussianPrioritySample == sampleSize:
                break
            pass
            indexOfGaussianPrioritySample += 1

        else:
            cToJudge = c
            weightNowPos, traverseEnd = getNextWeight(weightNowPos, initWeight, weightUpperBound, sideLength)
            if traverseEnd == True:
                break
            pass

        if sampleStrategy == "GaussianPrioritySample" or (weightNowPos-invVb).T.dot(V).dot(weightNowPos-invVb) <= cToJudge:
            i = i + 1
            EwEstimated = {}
            for edge in G.in_edges():
                indexEdge = edge2Index[edge]
                EwEstimated[(edge[0], edge[1])] = weightNowPos[indexEdge][0]/G[edge[0]][edge[1]]['weight']

            S = IM_oracle(G, EwEstimated, K)
            SpreadSize = IM_cal_reward(G, EwEstimated, S)

            if SpreadSize > BestReward:
                BestReward = SpreadSize
                BestS = S
                # BestWeight = copy.deepcopy(weightNowPos)
                BestEwEstimated = copy.deepcopy(EwEstimated)

    return BestS, BestEwEstimated

