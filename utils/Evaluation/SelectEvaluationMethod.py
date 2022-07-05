from config.ConfigEvaluation import EvaluationPara
from config.Config import PrivateSetting
from .EvaluationMethod import *
from .DrawPlot import *

def select_train_evaluation(totalNumbers:int, totalCorrect:int, totalEpoch:int, epoch:int) -> None:
    """
    According to configs in ConfigEvaluation, select evaluation methods for train.
    Note: Do not combine into other evaluaiton, cause too much if judge to do.
    
    Args:
        totalNumbers: total data amount
        totalCorrect: correctly predicted data amount
        totalEpoch: total epoch
        epoch: this epoch
    """
    if EvaluationPara.accuracy["switch"] and 'Train' in EvaluationPara.accuracy["mode"]:
        accuracy = eval_total_acc(totalNumbers, totalCorrect)
        if EvaluationPara.accuracy["saveTxt"]:
            save_acc_txt('Train', accuracy, epoch=epoch, totalEpoch=totalEpoch)
        if EvaluationPara.accuracy["saveJson"]:
            save_acc_json('Train', accuracy, epoch=epoch, totalEpoch=totalEpoch)   

def select_evaluation(task:str, totalNumbers:int, totalCorrect:int, perClassNumbers:list, perClassCorrect:list, className:list, resultList:list=None, totalEpoch:int=None, epoch:int=None) -> None:
    """
    According to configs in ConfigEvaluation, select evaluation methods for valid.

    Args:
        task: valid or test
        totalNumbers: total data amount
        totalCorrect: correctly predicted data amount
        perClassNumbers: amount of per class
        perClassCorrect: predicted correctly image amount of per class
        className: list of class name
        totalEpoch: total epoch
        epoch: this epoch
    """
    totalAccTxt  = totalAccJson  = None
    classAccTxt  = classAccJson  = None
    classNumTxt  = classNumJson  = None
    otherRateTxt = otherRateJson = None
    if EvaluationPara.accuracy["switch"] and task in EvaluationPara.accuracy["mode"]:
        accuracy = eval_total_acc(totalNumbers, totalCorrect)
        if EvaluationPara.accuracy["saveTxt"]:
            totalAccTxt = accuracy
        if EvaluationPara.accuracy["saveJson"]:
            totalAccJson = accuracy
    
    if EvaluationPara.accOfClasses["switch"] and task in EvaluationPara.accOfClasses["mode"]:
        perClassAccuracy = eval_class_acc(perClassNumbers, perClassCorrect, className)
        if EvaluationPara.accOfClasses["saveTxt"]:
            classAccTxt = perClassAccuracy
        if EvaluationPara.accOfClasses["saveJson"]:
            classAccJson = perClassAccuracy
    
    if EvaluationPara.numOfClasses["switch"] and task in EvaluationPara.numOfClasses["mode"]:
        perClassNum = show_num_acc(perClassNumbers, perClassCorrect, className)
        if EvaluationPara.accOfClasses["saveTxt"]:
            classNumTxt = perClassNum
        if EvaluationPara.accOfClasses["saveJson"]:
            classNumJson = perClassNum
    
    if EvaluationPara.otherClsRate["switch"] and task == 'Test':
        otherRate = eval_other_cls_rate(resultList, className,
                                        EvaluationPara.otherClsRate["posClass"], EvaluationPara.otherClsRate["negClass"])
        if EvaluationPara.otherClsRate["saveTxt"]:
            otherRateTxt = otherRate
        if EvaluationPara.otherClsRate["saveJson"]:
            otherRateJson = otherRate
    
    save_acc_txt(task, totalAccTxt, classAccTxt, classNumTxt, otherRateTxt, epoch=epoch, totalEpoch=totalEpoch)
    save_acc_json(task, totalAccJson, classAccJson, classNumJson, otherRateJson, epoch=epoch, totalEpoch=totalEpoch)

def select_valid_plot(accRecord:list) -> None:
    """
    According to configs in ConfigEvaluation, draw ValicAcc.

    Args:
        accRecord: list of acc for each epoch
    """
    if EvaluationPara.drawAccCurve["switch"]:
        draw_acc_curve(accRecord, PrivateSetting.outputPath)

def select_test_plot(cfMatrix, className: list) -> None:
    ### 阿阿阿世亞我普吉島cfMatrix是什麼型態, 雙重陣列type?
    """
    According to configs in ConfigEvaluation, draw cfMatrix.

    Args:
        cfMatrix: cfMatrix
        className: className: list of class name
    """
    if EvaluationPara.drawConfusionMatrix["switch"]:
        plot_confusion_matrix(cfMatrix=cfMatrix,
                              className=className,
                              showNumber=EvaluationPara.drawConfusionMatrix["showNumber"],
                              title='PredictedResult',
                              outputPath=PrivateSetting.outputPath)

def test_evaluation(resultList:list, classNameList:list) -> None:
    """
    Sum each record from resultList to evaluate

    Args:
        resultList: result list after model
        classNameList: className: list of class name
    """
    ##### sort class #####
    classNameList.sort()
    classNameList.sort(key=lambda x:x)

    ##### record #####
    totalCorrect = postProcessFilter = 0
    classCorrect = [0.] * len(classNameList)
    classTotal = [0.] * len(classNameList)
    cfMatrix = np.zeros([len(classNameList), len(classNameList)])
    for result in resultList:
        if not result["predict"] in classNameList:
            postProcessFilter += 1
        else:
            if result["predict"] == result["label"]:
                totalCorrect = totalCorrect + 1
                classCorrect[classNameList.index(result["label"])] += 1
            classTotal[classNameList.index(result["label"])] += 1
            cfMatrix[classNameList.index(result["label"])][classNameList.index(result["predict"])] += 1
    
    ##### evaluate #####
    select_evaluation(task='Test', totalNumbers=len(resultList)-postProcessFilter, totalCorrect=totalCorrect,
                      perClassNumbers=classTotal, perClassCorrect=classCorrect, className=classNameList, resultList=resultList)
    
    ##### print unknown rate #####
    if len(resultList) == 0:
        postProcessRate = 0
    else:
        postProcessRate = postProcessFilter/len(resultList)
    print(f'- Post Processing filters out {postProcessFilter} images: {postProcessRate*100:.4f} %')
    
    ##### draw cfMatrix #####
    select_test_plot(cfMatrix, className=classNameList)
