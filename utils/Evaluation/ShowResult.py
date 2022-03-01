from torch import eq, tensor
from config.Config import BasicSetting, PrivateSetting
from config.ConfigEvaluation import EvaluationPara


def show_total_acc(mode:str, total:int, totalCorrect:int):
    """
    Print accuracy for each epoch in terminal.

    Args:
        total: 總資料量
        totalCorrect: 分類正確的總數
    """
    if EvaluationPara.showAcc:
        print('{} acc: {:.4f} %'.format(mode, 100 * totalCorrect / total))
    

def show_class_acc(classTotal:list, classCorrect:list, className:list):
    for i, cls in enumerate(className):
        if classCorrect[i] == 0 and classTotal[i] == 0:
            classTotal[i] = 1
        print('- Accuracy of class {:.5s} : {:.4f} %'.format(cls, 100 * classCorrect[i] / classTotal[i]))


def show_num_data(classTotal:list, classCorrect:list):
    print("Total data for each class : ", classTotal)
    print("Correct data for each class: ", classCorrect)


def show_rate(total, totalCorrect, classTotal, classCorrect, cfMatrix, targetIndex):
    leakage = (sum(row[targetIndex] for row in cfMatrix) - cfMatrix[targetIndex][targetIndex]) / (total - classTotal[targetIndex]) * 100
    overkill = 100 - (100 * classCorrect[targetIndex] / classTotal[targetIndex])
    defectAcc = (totalCorrect - classCorrect[targetIndex]) / (total - classTotal[targetIndex]) * 100
    print("leakage: {:.4f}%, overkill: {:.4f}%, defectAcc: {:.4f}%".format(leakage, overkill, defectAcc))


def show_wrong_file(nameList, predict:tensor, labels:tensor, confidence:tensor, className, count:int):
    if EvaluationPara.showWrongFile:
        confidence = confidence.tolist()
        for i in range(len(predict)):
            fullname = nameList[count]
            count += 1
            if not eq(predict[i], labels[i]):
                print("Wrong file: {}, Label: {}, Pred: {}".format(fullname, className[int(labels[i])], className[int(predict[i])]))
                print("Confid: {}\n".format(confidence[i])) 
        return count
