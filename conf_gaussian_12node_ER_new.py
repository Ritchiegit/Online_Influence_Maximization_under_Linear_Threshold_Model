import os
import pickle
from Tool.create_save_path import *
from BanditAlg.IMLinUCB_LT import IMLinUCB_LT_Algorithm
from BanditAlg.OIM_ETC import OIM_ETC_Algorithm
import Oracle.EnumerateSeedsToGetHighestExpectation
oracle = Oracle.EnumerateSeedsToGetHighestExpectation.Enumerate_oracle
calculate_exact_spreadsize = Oracle.EnumerateSeedsToGetHighestExpectation.getSpreadSizeByProbability

seed_size = 3
iterationTimes = 6000

save_address = "SimulationResults/gaussian_12_ER"
create_save_path(save_address)

dataset = "ER_12Node_25Edge"
G = pickle.load(open(".//Datasets//ER_node12_p_0.2.G", 'rb'), encoding='latin1')
EwTrue = pickle.load(open(".//Datasets//ER_node12_p_0.2EWTrue.dic", 'rb'), encoding='latin1')

LinUCB_algs_name = 'LT-LinUCB'
sigma = 1
delta = 0.1

budgetList = [2, 5,
              10, 20, 50,
              100, 200]

# python Main.py --seed_size 3 --iterationTimes 6000 --save_address SimulationResults/gaussian_12_ER --G_address Datasets//ER_node12_p_0.2.G --weight_address Datasets/ER_node12_p_0.2EWTrue.dic
