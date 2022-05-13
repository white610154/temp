from config.ConfigEvaluation import EvaluationPara
from .ShowResult import *

def select_show_method(mode, dataSet, totalCorrect, classTotal, classCorrect, cfMatrix=None):
    """
    According to configs in ConfigEvaluation, select evaluation methods.
    """
    if EvaluationPara.showAcc["switch"]:
        show_total_acc(mode, len(dataSet), totalCorrect)
        
    if EvaluationPara.showClassAcc["switch"]:
        show_class_acc(classTotal, classCorrect, dataSet.className)

    if EvaluationPara.showNumOfClasses["switch"]:
        show_num_data(classTotal, classCorrect)
    
    if EvaluationPara.showRate["switch"]:
        targetIndex = []
        for name in EvaluationPara.showRate["targetClass"]:
            targetIndex.append(dataSet.className.index(name))
        show_rate(len(dataSet), totalCorrect, classTotal, classCorrect, cfMatrix, targetIndex)