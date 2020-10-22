import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
        tmpRes[i] = SumArrayInEachRound / (i + 1)
    return tmpRes

def draw_Regret_Folder(fileFolderForRead, fileFolderToSave, drawType="Default", Title=None, issave=False, isplot=True,
                       firstNum=300000, xmin=None, xmax=None, ymin=None, ymax=None, DrawList=None, RenameAlgs=None,
                       xlabel=None, ylabel=None):
    fileList = []
    for filename in os.listdir(fileFolderForRead):
        if (filename[-4:] == ".csv"):
            fileList.append(fileFolderForRead + "/" + filename)
    dataNpArray_list_dir = {}

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

        if RenameAlgs is None:
            if algsName == "LT-LinUCB":
                plt.plot(timeStamp, dataNpArrayAverage, label=algsName, linestyle='--')
            else:
                plt.plot(timeStamp, dataNpArrayAverage, label=algsName)
        else:
            if algsName == "LT-LinUCB":
                plt.plot(timeStamp, dataNpArrayAverage, label=algsName, linestyle='--')
            else:
                plt.plot(timeStamp, dataNpArrayAverage, label=RenameAlgs[i])
    plt.ylim(ymax=ymax, ymin=ymin)
    plt.xlim(xmax=xmax, xmin=xmin)
    plt.legend()
    if xlabel is None:
        plt.xlabel('Iteration')
    else:
        plt.xlabel(xlabel)

    if ylabel is None:
        plt.ylabel(drawType + " " + 'Regret')
    else:
        plt.ylabel(ylabel)
    if Title is not None:
        plt.title(Title)
    if issave:
        plt.savefig(fileFolderToSave + "/" + drawType + "WithErrorBar.png")
    if isplot:
        plt.show()
    plt.close("all")
