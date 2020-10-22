import sys
sys.path.append("..")

import VisualizationTools.draw_parameter_loss
import VisualizationTools.draw_Regret
import VisualizationTools.draw_Reward_Folder

round_to_plot = 20000

DrawList = ["LT-LinUCB", "budget=2", "budget=5","budget=10", "budget=20", "budget=50"] # ,"budget=100"]  # , "budget=200"]

AlgName_2_NewNameColorLinestyle = {
    "LT-LinUCB":("LT-LinUCB", "red", "--"),
    "budget=2":("OIM-ETC,k=2", "brown", "-"),
    "budget=5":("OIM-ETC,k=5", "deepskyblue", "-"),
    "budget=10":("OIM-ETC,k=10", "gold", "-"),
    "budget=20":("OIM-ETC,k=20", "limegreen", "-"),
    "budget=50":("OIM-ETC,k=50", "darkviolet", "-"),
    "budget=100":("OIM-ETC,k=100", "grey", "-"),
    "budget=200":("OIM-ETC,k=200", "k", "-"),
}
# DrawList = None


fileFolderSum = '../SimulationResults/BinarySelect2_100100_2d'
fileFolderForRead = fileFolderSum + '/Reward'
fileFolderToSave = fileFolderSum + '/Reward'
drawType = "Average"  # "Cumulative" "Average" "Default"
# TODO
VisualizationTools.draw_Reward_Folder.draw_Reward_Folder(fileFolderForRead, fileFolderToSave, drawType=drawType, issave=True, isplot=True, firstNum=round_to_plot, DrawList=DrawList, xlabel="Round t", ylabel="Average Reward", AlgName_2_NewNameColorLinestyle=AlgName_2_NewNameColorLinestyle, Title="(b)")

"""
# 需要限制所有实验结果文件都达到firstNum轮，才能绘制
fileFolderForRead = fileFolderSum + '/ParameterLoss'
fileFolderToSave = fileFolderSum + '/ParameterLoss'
drawType = "Default"  # "Cumulative" "Average" "Default"
VisualizationTools.draw_parameter_loss.draw_Parameter_Folder(fileFolderForRead, fileFolderToSave, drawType=drawType, issave=True, isplot=False, firstNum=4000, DrawList=DrawList)

fileFolderForRead = fileFolderSum + '/Regret'
fileFolderToSave = fileFolderSum + '/Regret'
drawType = "Cumulative"  # "Cumulative" "Average" "Default"
VisualizationTools.draw_Regret.draw_Regret_Folder(fileFolderForRead, fileFolderToSave, drawType=drawType, issave=True, isplot=False, firstNum=4000, DrawList=DrawList)  # , ymin=-10, ymax=1500  )
"""
