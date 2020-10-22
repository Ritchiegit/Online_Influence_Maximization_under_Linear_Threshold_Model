import os
import pickle
from Tool.create_save_path import *
from BanditAlg.IMLinUCB_LT_little_V_binary_2d import IMLinUCB_LT_Algorithm
from BanditAlg.OIM_ETC import OIM_ETC_Algorithm
import Oracle.BinaryOracle
oracle = Oracle.BinaryOracle.getOracleOfBinary  # 选出最优种子
calculate_exact_spreadsize = Oracle.BinaryOracle.getSpreadOfBinary

seed_size = 5
iterationTimes = 22000

save_address = "SimulationResults/BinarySelect2_100100_2d"
create_save_path(save_address)

dataset = "DIY_Binary_RandomSelect2_100_100"
G = pickle.load(open(".//Datasets//DIY_Binary_RandomSelect2_100_100.G", 'rb'), encoding='latin1')
EwTrue = pickle.load(open(".//Datasets//DIY_Binary_RandomSelect2_100_100EWTrue.dic", 'rb'), encoding='latin1')

LinUCB_algs_name = 'LT-LinUCB-2d'
sigma = 1
delta = 0.1

budgetList = [1, 2, 3, 4, 5, 6,
              10, 20, 50,
              100, 200, 300, 400, 500,
              1000]

# python Main.py --is_bipartite --seed_size 5 --iterationTimes 22000 --save_address SimulationResults/BinarySelect2_100100_2d --G_address Datasets//DIY_Binary_RandomSelect2_100_100.G --weight_address Datasets/DIY_Binary_RandomSelect2_100_100EWTrue.dic