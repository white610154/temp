from config.ConfigEvaluation import EvaluationPara
from .ShowResult import *

def select_show_method(mode, dataSet, totalCorrect, classTotal, classCorrect,
                       cfMatrix, predicted, labels, confidence=None, count=None):
    if EvaluationPara.showAcc:
        show_total_acc(mode, len(dataSet), totalCorrect)
        
    if EvaluationPara.showClassAcc:
        show_class_acc(classTotal, classCorrect, dataSet.className)

    if EvaluationPara.showNumOfClasses:
        show_num_data(classTotal, classCorrect)
    
    if EvaluationPara.showRate['switch']:
        show_rate(len(dataSet), totalCorrect, classTotal, classCorrect,
                  cfMatrix, dataSet.className.index(EvaluationPara.showRate['targetIndex']))
    
    if EvaluationPara.showWrongFile:
        show_wrong_file(dataSet.filename, predicted, labels, confidence, dataSet.className, count)