import json
import os
from config.Config import PrivateSetting ### 阿阿阿世亞對不起這個沒有搬到呀, 交給你了

def create_folder() -> None:
    """
    create a folder which did not exist
    """
    if not os.path.isdir(PrivateSetting.outputPath):
        os.makedirs(PrivateSetting.outputPath)

def eval_total_acc(totalNumbers:int, totalCorrect:int) -> float:
    """
    Evaluate total accuracy

    Args:
        totalNumbers: total data amount
        totalCorrect: correctly predicted data amount

    Return:
        accuracy
    """
    if totalNumbers == 0:
        accuracy = 0
    else:
        accuracy = float(totalCorrect / totalNumbers)
    print(f'- Accuracy: {100 * accuracy:.4f} %')
    return float(accuracy)

def eval_class_acc(perClassNumbers:list, perClassCorrect:list, className:list) -> dict:
    """
    Evaluate accuracy for each class

    Args:
        perClassNumbers: list of data amount for each class
        perClassCorrect: list of correctly predicted data amount for each class
        className: list of each class name
    
    Return:
        perClassAccuracy: dict of each class accuracy
    """
    perClassAccuracy = {}
    for i, c in enumerate(className):
        if perClassNumbers[i] == 0:
            perClassAccuracy[c] = 0
        else:
            perClassAccuracy[c] = float(perClassCorrect[i] / perClassNumbers[i])
        print(f'- Accuracy of class {c:.5s} : {100 * perClassAccuracy[c]:.4f} %')
    return perClassAccuracy

def show_num_acc(perClassNumbers:list, perClassCorrect:list, className:list) -> dict:
    """
    Show data amount and correctly predicted data amount for each class

    Args:
        perClassNumbers: list of data amount for each class
        perClassCorrect: list of correctly predicted data amount for each class
        className: list of each class name
    
    Return:
        classNum: dict of className, perClassNumbers and perClassCorrect
    """
    print('- Class Name: ', className)
    print('- Total data for each class: ', perClassNumbers)
    print('- Correct data for each class: ', perClassCorrect)
    classNum = {
        "Name": className,
        "Numbers": perClassNumbers,
        "Correct": perClassCorrect
    }
    return classNum

def eval_other_cls_rate(resultList:list, className:list, posClass:list, negClass:list) -> dict:
    """
    Evaluate leakage, overkill, defectAccuracy

    Args:
        resultList: list of prediction
        className: list of each class name 
        posClass: list of positive classes
        negClass: list of negative classes

    Return:
        otherRate: dict of leakage, overkill and defectAccuracy  
    """
    if len(posClass) == 0 or len(negClass) == 0:
        raise BaseException('The posClass and negClass should not be empty. Please check otherClsRate in config/ConfigEvaluation.py.')
    posClass.sort()
    posClass.sort(key=lambda x:x)
    negClass.sort()
    negClass.sort(key=lambda x:x)
    
    defectNumbers = [0.] * len(negClass)
    defectCorrect = [0.] * len(negClass)
    leakageNumbers = leakageCorrect = overkillNumbers = overkillCorrect = 0
    for result in resultList:
        if result["label"] in negClass:
            leakageNumbers = leakageNumbers + 1
            if result["predict"] in negClass:
                leakageCorrect = leakageCorrect + 1
                defectNumbers[negClass.index(result["label"])] += 1
                if result["predict"] == result["label"]:
                    defectCorrect[negClass.index(result["label"])] += 1
        if result["label"] in posClass:
            overkillNumbers = overkillNumbers + 1
            if result["predict"] in posClass:
                overkillCorrect = overkillCorrect + 1
    
    if leakageNumbers == 0:
        leakageRate = 0
    else:
        leakageRate = (leakageNumbers  - leakageCorrect)  / leakageNumbers
    if overkillNumbers == 0:
        overkillRate = 0
    else:
        overkillRate = (overkillNumbers - overkillCorrect) / overkillNumbers
    
    defectAccuracy = {}
    for i, neg in enumerate(negClass):
        if defectNumbers[i] == 0:
            defectAccuracy[neg] = 0
        else:
            defectAccuracy[neg] = defectCorrect[i] / defectNumbers[i]

    otherRate = {
        "Leakage" : leakageRate,
        "Overkill": overkillRate,
        "DefectAccuracy": defectAccuracy
    }
    print(f'- Leakage Rate: {100 * otherRate["Leakage"]:.4f} %')
    print(f'- Overkill Rate: {100 * otherRate["Overkill"]:.4f} %')
    for i in range(len(defectAccuracy)):
        print(f'- Defect accuracy of class {list(defectAccuracy.keys())[i]:.5s} : {100 * list(defectAccuracy.values())[i]:.4f} %')
    return otherRate
    
def save_acc_txt(task:str, accuracy:float=None, classAccuracy:dict=None, classNum:dict=None, otherRate:dict=None, epoch:int=None, totalEpoch:int=None) -> None:
    """
    Save evaluation rate to txt

    Args:
        task: Train, Valid or Test
        epoch: epoch
        totalEpoch: totalEpoch
        accuracy: accuracy
        classAccuracy: dict of accuracy for each class
        classNum: dict of name for each class, correctly predicted data amount for each class, total data amount for each class
        otherRate: leakage rate, overkill rate, accuracy for each defect class

    Return:
    Save TrainAcc.txt, ValidAcc.txt or TestAcc.txt
    """
    
    if accuracy != None or classAccuracy != None or classNum != None or otherRate != None:
        create_folder()

        ##### Set file and title #####
        txtFilePath = f'./{PrivateSetting.outputPath}/{task}Acc.txt'
        if epoch == None:
            accTxt = open(txtFilePath, 'w')
            print('{task}', file=accTxt)
        else:
            if epoch == 0:
                accTxt = open(txtFilePath, 'w')
            else:
                accTxt = open(txtFilePath, 'a')
            print(f'{task} epoch {epoch+1} / {totalEpoch}', file=accTxt)
        
        ##### Save each record #####
        if accuracy:
            print(f'- Accuracy: {100 * accuracy:.4f} %', file=accTxt)
        if classAccuracy:
            for i in range(len(classAccuracy)):
                print(f'- Accuracy of class {list(classAccuracy.keys())[i]:.5s} : {100 * list(classAccuracy.values())[i]:.4f} %', file=accTxt)
        if classNum:
            print(f'- Class Name: {classNum["Name"]}', file=accTxt)
            print(f'- Total data for each class: {classNum["Numbers"]}', file=accTxt)
            print(f'- Correct data for each class: {classNum["Correct"]}', file=accTxt)
        if otherRate:
            print(f'- Leakage Rate: {100 * otherRate["Leakage"]:.4f} %', file=accTxt)
            print(f'- Overkill Rate: {100 * otherRate["Overkill"]:.4f} %', file=accTxt)
            for i in range(len(otherRate["DefectAccuracy"])):
                print(f'- Defect accuracy of class {list(otherRate["DefectAccuracy"].keys())[i]:.5s} : {100 * list(otherRate["DefectAccuracy"].values())[i]:.4f} %', file=accTxt)
        print('', file=accTxt)
        
def save_acc_json(task:str, accuracy:float=None, classAccuracy:float=None, classNum:float=None, otherRate:dict=None, epoch:int=None, totalEpoch:int=None) -> None:
    """
    Save evaluation rate to json

    Args:
        task: Train, Valid or Test
        accuracy: accuracy
        classAccuracy: dict of accuracy for each class
        classNum: dict of name for each class, correctly predicted data amount for each class, total data amount for each class
        otherRate: leakage rate, overkill rate, accuracy for each defect class
        epoch: epoch
        totalEpoch: totalEpoch

    Return:
    Save TrainAcc.json, ValidAcc.json or TestAcc.json
    """
    if accuracy != None or classAccuracy != None or classNum != None or otherRate != None:
        create_folder()
        jsonFilePath = f'./{PrivateSetting.outputPath}/{task}Acc.json'

        ##### Save each record ##### 
        epochDict = {}
        epochDict[task] = {}
        if accuracy:   
            epochDict[task]["accuracy"] = accuracy
        if classAccuracy:
            epochDict[task]["classAccuracy"] = classAccuracy
        if classNum:
            epochDict[task]["className"] = classNum["Name"]
            epochDict[task]["classNumbers"] = classNum["Numbers"]
            epochDict[task]["classCorrect"] = classNum["Correct"]
        if otherRate:
            epochDict[task]["Leakage"] = otherRate["Leakage"]
            epochDict[task]["Overkill"] = otherRate["Overkill"]
            epochDict[task]["DefectAccuracy"] = otherRate["DefectAccuracy"]
        ##### only for SALA platform #####
        if task == 'Test':
            epochDict[task]["ConfusionMatrix"] = f'./{PrivateSetting.outputPath}/ConfusionMatrix.jpg'
        
        ##### Save record to json #####
        infoDict = {}
        if epoch == None:
            infoDict[task] = epochDict
        else:
            if epoch != 0:
                with open(jsonFilePath, 'r') as accJson:
                    infoDict = json.load(accJson)
            epochDict["model"] = {
                "epoch": epoch + 1,
                "total": totalEpoch
                }
            infoDict[str(epoch + 1)] = epochDict
        with open(jsonFilePath, 'w') as accJson:
            json.dump(infoDict, accJson, indent=4)
