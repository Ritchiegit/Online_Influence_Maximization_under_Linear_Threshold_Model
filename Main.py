import os
import pickle
import argparse
import time
import random
import numpy as np
import datetime
import LT.LT
import Oracle.EnumerateSeedsToGetHighestExpectation
import Oracle.BinaryOracle
from Tool.create_save_path import *
from BanditAlg.OIM_ETC import OIM_ETC_Algorithm
from BanditAlg.IMLinUCB_LT import IMLinUCB_LT_Algorithm as IMLinUCB_LT_Algorithm_TS
from BanditAlg.IMLinUCB_LT_little_V_binary_2d import IMLinUCB_LT_Algorithm as IMLinUCB_LT_Algorithm_2d



class simulateOnlineData:
    def __init__(self, G, EwTrue, seed_size, oracle, calculate_exact_spreadsize, iterationTime, dataset, RandomSeed):
        self.G = G
        self.EwTrue = EwTrue  # True weight
        self.seed_size = seed_size
        self.oracle = oracle
        self.calculate_exact_spreadsize = calculate_exact_spreadsize
        self.iterationTime = iterationTime
        self.dataset = dataset
        self.RandomSeed = RandomSeed
        self.startTime = datetime.datetime.now()
        self.AlgReward = {}
        self.AlgLoss = {}
        self.AlgRegret = {}

    def runAlgorithms(self, algorithms):
        self.tim_ = []
        for alg_name, alg in list(algorithms.items()):
            self.AlgReward[alg_name] = []
            self.AlgLoss[alg_name] = []
            self.AlgRegret[alg_name] = []

        self.resultRecord()
        BestSeedSet = self.oracle(self.G, self.EwTrue, self.seed_size)
        BestSpreadSize = self.calculate_exact_spreadsize(self.G, self.EwTrue, BestSeedSet)

        for iter_ in range(self.iterationTime):
            for alg_name, alg in list(algorithms.items()):
                # 1. use Online Algs to decide seed
                print("\n1. Get seed with Online Algs")
                S, EwEstimated = alg.decide()
                print("seed set", S)  # list

                # 2. get live_edge/node from LT
                # observe edge level feedback
                print("2. Simulate Influence Spreading on LT")
                reward, finalInfluencedNodeList, workedInNodeList, attemptingActivateInNodeDir, ActivateInNodeOfFinalInfluencedNodeListDir_AMomentBefore = LT.LT.runLT_NodeFeedback(
                    G, S, EwTrue)
                print("Simulated Result: size is", reward)

                # 2 get Reward
                print("2. Get Expectation Reward of Algs Seeds")
                reward = self.calculate_exact_spreadsize(self.G, self.EwTrue, S)
                print("Expected Reward: size is", reward)

                # 3. Update parameters A b
                print("3. Update parameters A b")
                alg.updateParameters(finalInfluencedNodeList, attemptingActivateInNodeDir,
                                     ActivateInNodeOfFinalInfluencedNodeListDir_AMomentBefore)

                # 4. Record results
                self.AlgReward[alg_name].append(reward)
                self.AlgRegret[alg_name].append(BestSpreadSize - reward)
                self.AlgLoss[alg_name].append(alg.getLoss()[-1])

            self.resultRecord(iter_)
        print("No", iter_, ":Average Oracle Reward", BestSpreadSize)
        print("Best Seed Set", BestSeedSet)

    def resultRecord(self, iter_=None):
        if iter_ is None:
            # Initialize the header
            timeRun = self.startTime.strftime('_%m_%d_%H_%M_%S')
            fileSig = '_seedsize' + str(self.seed_size) + '_iter' + str(self.iterationTime) + '_' + self.dataset + "_RandomSeed" + str(RandomSeed)

            self.filenameWriteReward = os.path.join(save_address, 'Reward/Reward' + timeRun + fileSig + '.csv')
            with open(self.filenameWriteReward, 'w') as f:
                f.write('Time(Iteration)')
                f.write(',' + ','.join([str(alg_name) for alg_name in algorithms.keys()]))
                f.write('\n')

            self.filenameWriteParameterLoss = os.path.join(save_address, 'ParameterLoss/Lossweight' + timeRun + fileSig + '.csv')
            with open(self.filenameWriteParameterLoss, 'w') as f:
                f.write('Time(Iteration)')
                f.write(',' + ','.join([str(alg_name) for alg_name in algorithms.keys()]))
                f.write('\n')

            self.filenameWriteRegret = os.path.join(save_address, 'Regret/Regret' + timeRun + fileSig + '.csv')
            with open(self.filenameWriteRegret, 'w') as f:
                f.write('Time(Iteration)')
                f.write(',' + ','.join([str(alg_name) for alg_name in algorithms.keys()]))
                f.write('\n')
        else:
            print("Iteration %d" % iter_, " Elapsed time", datetime.datetime.now() - self.startTime)
            self.tim_.append(iter_)
            with open(self.filenameWriteReward, 'a+') as f:
                f.write(str(iter_))
                f.write(
                    ',' + ','.join([str(self.AlgReward[alg_name][-1]) for alg_name in algorithms.keys()]))  # Record the last number
                f.write('\n')

            with open(self.filenameWriteParameterLoss, 'a+') as f:
                f.write(str(iter_))
                f.write(
                    ',' + ','.join([str(self.AlgLoss[alg_name][-1]) for alg_name in algorithms.keys()]))
                f.write('\n')

            with open(self.filenameWriteRegret, 'a+') as f:
                f.write(str(iter_))
                f.write(
                    ',' + ','.join([str(self.AlgRegret[alg_name][-1]) for alg_name in algorithms.keys()]))
                f.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--is_bipartite', action='store_true', default=False)
    parser.add_argument("--seed_size", type=int, default=1, help="")
    parser.add_argument("--iterationTimes", type=int, default=50, help="")
    parser.add_argument("--save_address", type=str, default="SimulationResults/gaussian_9_ER", help="")
    parser.add_argument("--dataset_name", type=str, default="", help="")
    parser.add_argument("--G_address", type=str, default="Datasets/ER_node9_p_0.2.G", help="")
    parser.add_argument("--weight_address", type=str, default="Datasets/ER_node9_p_0.2EWTrue.dic", help="")
    parser.add_argument("--LinUCB_algs_name", type=str, default="LT-LinUCB", help="")
    parser.add_argument("--budgetList", nargs='*', default=[2, 5, 10, 20, 50, 100, 200])
    args = parser.parse_args()
    budgetList = []
    for budget_each in args.budgetList:
        budgetList.append(int(budget_each))
    print(budgetList)
    print(args.budgetList)

    if args.is_bipartite == True:
        oracle = Oracle.BinaryOracle.getOracleOfBinary
        calculate_exact_spreadsize = Oracle.BinaryOracle.getSpreadOfBinary
        IMLinUCB_LT_Algorithm = IMLinUCB_LT_Algorithm_2d

    else:
        oracle = Oracle.EnumerateSeedsToGetHighestExpectation.Enumerate_oracle
        calculate_exact_spreadsize = Oracle.EnumerateSeedsToGetHighestExpectation.getSpreadSizeByProbability
        IMLinUCB_LT_Algorithm = IMLinUCB_LT_Algorithm_TS


    seed_size = args.seed_size
    iterationTimes = args.iterationTimes
    save_address = args.save_address
    create_save_path(save_address)
    dataset_name = args.dataset_name
    G = pickle.load(open(args.G_address, 'rb'), encoding='latin1')
    EwTrue = pickle.load(open(args.weight_address, 'rb'), encoding='latin1')
    LinUCB_algs_name = args.LinUCB_algs_name
    sigma = 1
    delta = 0.1

    # Fix numpy seed for reproducibility
    RandomSeed = int(time.time() * 100) % 399
    print("RandomSeed = %d" % RandomSeed)
    np.random.seed(RandomSeed)
    random.seed(RandomSeed)

    print("Num of nodes", len(G.nodes))
    print("Num of edges", len(G.in_edges))

    simExperiment = simulateOnlineData(G, EwTrue, seed_size, oracle, calculate_exact_spreadsize, iterationTimes, dataset_name, RandomSeed)
    algorithms = {}

    algorithms[LinUCB_algs_name] = IMLinUCB_LT_Algorithm(G, EwTrue, seed_size, iterationTimes, sigma, delta, oracle, calculate_exact_spreadsize)

    for budgetTime in budgetList:
        algorithms['budget=' + str(budgetTime)] = OIM_ETC_Algorithm(G, EwTrue, seed_size, oracle, iterationTimes,
                                                                    budgetTime=budgetTime)

    simExperiment.runAlgorithms(algorithms=algorithms)
