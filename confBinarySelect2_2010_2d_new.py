
import os
import pickle
from Tool.create_save_path import *
from BanditAlg.IMLinUCB_LT_little_V_binary_2d import IMLinUCB_LT_Algorithm
from BanditAlg.OIM_ETC import OIM_ETC_Algorithm
import Oracle.BinaryOracle
oracle = Oracle.BinaryOracle.getOracleOfBinary
calculate_exact_spreadsize = Oracle.BinaryOracle.getSpreadOfBinary

seed_size = 3
iterationTimes = 30000

save_address = "SimulationResults/BinarySelect2_2010_2d"
create_save_path(save_address)

dataset = "DIY_Binary_RandomSelect2_20_10"
G = pickle.load(open(".//Datasets//DIY_Binary_RandomSelect2_20_10.G", 'rb'), encoding='latin1')
EwTrue = pickle.load(open(".//Datasets//DIY_Binary_RandomSelect2_20_10EWTrue.dic", 'rb'), encoding='latin1')

LinUCB_algs_name = 'LT-LinUCB-2d'
sigma = 1
delta = 0.1

budgetList = [2, 5,
              10, 20, 50,
              100, 200]

# python Main.py --is_bipartite --seed_size 3 --iterationTimes 30000 --save_address SimulationResults/BinarySelect2_2010_2d --G_address Datasets//DIY_Binary_RandomSelect2_20_10.G --weight_address Datasets/DIY_Binary_RandomSelect2_20_10EWTrue.dic
