import numpy as np

from torch import eq, tensor
from config.Config import BasicSetting, PrivateSetting
from config.ConfigEvaluation import EvaluationPara


def show_total_acc(mode:str, total:int, totalCorrect:int):
    """
    Show overall accuracy for each epoch in terminal.

    Args:
        mode: title show in terminal
        total: total data amount
        totalCorrect: correctly predicted data amount
    """
    if EvaluationPara.showAcc:
        print('{} acc: {:.4f} %'.format(mode, 100 * totalCorrect / total))
    

def show_class_acc(classTotal:list, classCorrect:list, className:list):
    """
    Show accuracy of each class in terminal.

    Args:
        classTotal: data amount of each class
        classCorrect: correctly predicted data amount of each class
        className: class name of each class
    """
    for i, cls in enumerate(className):
        if classCorrect[i] == 0 and classTotal[i] == 0:
            classTotal[i] = 1
        print('- Accuracy of class {} : {:.4f} %'.format(cls, 100 * classCorrect[i] / classTotal[i]))


def show_num_data(classTotal:list, classCorrect:list):
    """
    Show data amount and correctly predicted amount of each class in terminal.

    Args:
        classTotal: data amount of each class
        classCorrect: correctly predicted data amount of each class
    """
    print('Total data for each class : ', classTotal)
    print('Correct data for each class: ', classCorrect)


def show_rate(total, totalCorrect, classTotal, classCorrect, cfMatrix, targetIndex):
    """
    Show leakage, overkill, defectAcc in terminal.

    Args:
        total: total data amount
        totalCorrect: correctly predicted data amount
        classTotal: data amount of each class
        classCorrect: correctly predicted data amount of each class
        cfMatrix: confusion matrix
        targetIndex: the class index of "OK" or "Pass" in the className list 
    """
    if len(targetIndex) == len(classTotal):
        raise BaseException('The targetClass should not include all class. Please check showRate["targetClass"] in config/ConfigEvaluation.py.')
    predictPass = 0
    correctPass = 0
    totalPass = 0
    wrongPass = 0
    actualPass = 0
    for index1 in targetIndex:
        predictPass += sum(row[index1] for row in cfMatrix)
        correctPass += cfMatrix[index1][index1]
        totalPass += classTotal[index1]
        actualPass += classCorrect[index1]
        for index2 in targetIndex:
            if index1 == index2:
                continue
            wrongPass += cfMatrix[index2][index1]
    leakageRate = (predictPass - correctPass - wrongPass) / (total - totalPass) * 100
    overkillRate = 100 - ((actualPass + wrongPass) / totalPass * 100)
    defectAcc = (totalCorrect - correctPass) / (total - totalPass) * 100
    print('leakage: {:.4f}%, overkill: {:.4f}%, defectAcc: {:.4f}%'.format(leakageRate, overkillRate, defectAcc))


def show_wrong_file(nameList, predict:tensor, labels:tensor, confidence:tensor, className, count:int):
    """
    Show the file names of incorrectly predict datas.

    Args:
        nameList: list include all file names
        predict: model prediction (dtype: tensor)
        labels: correct label (dtype:tensor)
        confidence: predicted confidence
        className: class name of each class
        count: use to record current file
    """
    if EvaluationPara.showWrongFile["switch"]:
        confid = confidence.cpu().numpy()
        confid = confid[:, :len(className)]
        for i in range(len(predict)):
            fullname = nameList[count]
            count += 1
            if not eq(predict[i], labels[i]):
                print('Wrong file: {}, Label: {}, Pred: {}'.format(fullname, className[int(labels[i])], className[int(predict[i])]))
                print('Confid: {}\n'.format(confid[i])) 
        return count
