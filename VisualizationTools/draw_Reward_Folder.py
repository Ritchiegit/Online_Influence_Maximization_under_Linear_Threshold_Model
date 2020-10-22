import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os


def array2CumulativeArray(rawArray):
    tmpRes = np.zeros(len(rawArray))
    SumArrayInEachRound = 0
    for i in range(len(rawArray)):
        SumArrayInEachRound += rawArray[i]
        tmpRes[i] = SumArrayInEachRound
    return tmpRes
def array2AverageArray(rawArray):
    tmpRes = np.zeros(len(rawArray))
    SumArrayInEachRound = 0
    for i in range(len(rawArray)):
        SumArrayInEachRound += rawArray[i]
        tmpRes[i] = SumArrayInEachRound / (i+1)
    return tmpRes

def draw_Reward_Folder(fileFolderForRead, fileFolderToSave, drawType="Default", Title=None, issave=False, isplot=False,
                       firstNum=10000, xmin=None, xmax=None, ymin=None, ymax=None, DrawList=None, RenameAlgs=None,
                       xlabel=None, ylabel=None, AlgName_2_NewNameColorLinestyle=None):
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    fileList = []
    for filename in os.listdir(fileFolderForRead):
        if (filename[-4:] == ".csv"):
            fileList.append(fileFolderForRead + "/" + filename)
    dataNpArray_list_dir = {}
    newfileList = []
    for fileTotalPath in fileList:
        dataInFrame = pd.read_csv(fileTotalPath)
        if dataInFrame["Time(Iteration)"].values.shape[0] >= firstNum:
            newfileList.append(fileTotalPath)
    if len(newfileList) > 0:
        fileList = newfileList
        print("There are {} files with enough rounds".format(len(newfileList)))
    else:
        print("There is no files with enough rounds")
        return

    firstFilePath = fileList[0]
    dataInFrame = pd.read_csv(firstFilePath)
    for algsName in dataInFrame:
        if algsName == "Time(Iteration)":
            continue
        dataNpArray_list_dir[algsName] = []
    timeStamp = np.arange(1, dataInFrame["Time(Iteration)"].values.shape[0] + 1)[:firstNum]

    for fileTotalPath in fileList:
        dataInFrame = pd.read_csv(fileTotalPath)
        for algsName in dataInFrame:
            if algsName == "Time(Iteration)":
                continue
            dataNpArray = dataInFrame[algsName].values[:firstNum]
            if drawType == "Cumulative":
                dataNpArray = array2CumulativeArray(dataNpArray)
            elif drawType == "Average":
                dataNpArray = array2AverageArray(dataNpArray)
            else:
                pass

            dataNpArray_list_dir[algsName].append(dataNpArray)
    i = -1
    for algsName in dataNpArray_list_dir:
        if DrawList is None:
            pass
        else:
            if algsName in DrawList:
                pass
            else:
                continue
        i += 1
        dataNpArrayAll = np.vstack(dataNpArray_list_dir[algsName])
        dataNpArrayAverage = np.mean(dataNpArrayAll, axis=0)

        if AlgName_2_NewNameColorLinestyle != None:
            if algsName in AlgName_2_NewNameColorLinestyle:
                plt.plot(timeStamp, dataNpArrayAverage, label=AlgName_2_NewNameColorLinestyle[algsName][0],
                         color=AlgName_2_NewNameColorLinestyle[algsName][1], linestyle=AlgName_2_NewNameColorLinestyle[algsName][2])
        else:
            plt.plot(timeStamp, dataNpArrayAverage, label=algsName)

    plt.ylim(ymax=ymax, ymin=ymin)
    plt.xlim(xmax=xmax, xmin=xmin)
    plt.legend(loc=4)
    if xlabel is None:
        plt.xlabel('Iteration')
    else:
        plt.xlabel(xlabel)

    if ylabel is None:
        plt.ylabel(drawType + " " + 'Reward')
    else:
        plt.ylabel(ylabel)

    if Title is not None:
        plt.title(Title)
    if issave:
        pp = PdfPages(fileFolderToSave+"/" + drawType + "2WithErrorBar.pdf")
        pp.savefig()
        plt.savefig(fileFolderToSave+"/" + drawType + "2WithErrorBar.png")
        pp.close()
    if isplot:
        plt.show()
    else:
        plt.close("all")
