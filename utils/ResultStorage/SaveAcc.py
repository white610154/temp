import os, json
from torch import tensor
from config.Config import BasicSetting, PrivateSetting
from config.ConfigResultStorage import ResultStorage
from .csvModule import UsingCsv

def save_epoch_acc_txt(epoch:int, total:int, totalCorrect:int, classTotal:list, classCorrect:list, className:list):
    """
    Save epoch accuracy and class accuracy into txt file.

    Args:
        epoch: current epoch number
        total: total data amount
        totalCorrect: correctly predicted data amount
        classTotal: data amount of each class
        classCorrect: correctly predicted data amount of each class
        className: list of class name
    Return:
        ValidAcc.txt
    """
    if ResultStorage.saveAccTxt["switch"]:
        if epoch == 0:
            with open(f'./{PrivateSetting.outputPath}/ValidAcc.txt','w') as fAcc:
                print('Validation acc of epoch {}: {:.4f} %'.format(epoch+1, 100 * totalCorrect / total), file = fAcc)
                for i, cls in enumerate(className):
                    print('- Accuracy of class {:.5s} : {:.4f} %'.format(cls, 100 * classCorrect[i] / classTotal[i]), file = fAcc)
        else:
            with open(f'./{PrivateSetting.outputPath}/ValidAcc.txt','a') as fAcc:
                print('\nValidation acc of epoch {}: {:.4f} %'.format(epoch+1, 100 * totalCorrect / total), file = fAcc)
                for i, cls in enumerate(className):
                    print('- Accuracy of class {:.5s} : {:.4f} %'.format(cls, 100 * classCorrect[i] / classTotal[i]), file = fAcc)


def save_epoch_acc_json(epoch:int, totalEpoch: int, total:int, totalCorrect:int, classTotal:list, classCorrect:list, className:list):
    """
    Save epoch accuracy and class accuracy into json file.

    Args:
        epoch: current epoch number
        totalEpoch: total epoch number
        total: total data amount
        totalCorrect: correctly predicted data amount
        classTotal: data amount of each class
        classCorrect: correctly predicted data amount of each class
        className: list of class name
    Return:
        modelTraining.json
    """
    jsonFilePath = f'./{PrivateSetting.outputPath}/modelTraining.json'
    classAccDict = {}
    for i, cls in enumerate(className):
        classAccDict[cls] = 100 * classCorrect[i] / classTotal[i]
    epochDict = {
        "model": {
            "epoch": epoch + 1,
            "total": totalEpoch
        },
        "valid": {
            "accuracy": totalCorrect / total,
            "classAccuracy": classAccDict
        }
    }
    infoDict = {}
    if epoch != 0:
        if os.path.exists(jsonFilePath):
            with open(jsonFilePath, 'r') as fAcc:
                infoDict = json.load(fAcc)
    infoDict[str(epoch + 1)] = epochDict
    with open(jsonFilePath, 'w') as fAcc:
        json.dump(infoDict, fAcc, indent=4)


def output_result_csv(nameList:list, predict:tensor, labels:tensor, confidence:tensor, className:list, count:int, mode=BasicSetting.task):
    """
    Output test result into csv file, file name : Test_result.csv or Inference_result.csv.

    Args:
        nameList: list include all file names
        predict: model prediction (dtype: tensor)
        labels: correct label (dtype:tensor)
        confidence: predicted confidence
        className: class name of each class
        count: use to record current file

    format in csv file: 
        Filename | Ground truth | Prediction | Confidence of each class

    """
    if ResultStorage.savePredictResult["switch"]:
        ### Create csv file and title
        if mode == "Test":
            fileName = 'Test_result.csv'
            title = ['Filename', 'Ground truth', 'Prediction']
        elif mode == "Inference":
            fileName = 'Inference_result.csv'
            title = ['Filename', 'Prediction']

        title.extend(className)
        saveAccCsv = UsingCsv(fileName, PrivateSetting.outputPath , title)
        if count == 0 :
            saveAccCsv.create_csv()

        ### Write result to csv file
        confidence = confidence.tolist()
        for i in range(len(predict)):
            fullname = nameList[count]
            if mode == "Test":
                result = [fullname, className[int(labels[i])], className[int(predict[i])]]
            elif mode == "Inference":
                result = [fullname, className[int(predict[i])]]
            result.extend(confidence[i][:len(className)])
            saveAccCsv.writing(result, 'a')
            count += 1
        return count

def unknown_threshold(nameList, predict:tensor, labels:tensor, confidence:tensor, className, count:int, mode=BasicSetting.task):
    """
    Filter out images with scores below the threshold 

    Args:
        nameList: list include all file names
        predict: model prediction (dtype: tensor)
        labels: correct label (dtype:tensor)
        confidence: predicted confidence
        className: class name of each class  
        count: use to record current file
    """
    if ResultStorage.unknownFilter["switch"]:
        filterDict = ResultStorage.unknownFilter["filter"]  # {tagName:threshold}
        reverse = ResultStorage.unknownFilter["reverse"]
        filter = sorted(filterDict.items(), key=lambda x:x[1], reverse=reverse) # x[1]: score
        if mode == "Test":
            fileName = f'Test_filter.csv' 
            title = ['Filename', 'Ground truth', 'Prediction', 'sorce']
        else:
            fileName = f'Inference_filter.csv'
            title = ['Filename', 'Prediction', 'sorce']

        unknownCsv = UsingCsv(fileName, PrivateSetting.outputPath, title)
        if count == 0 and ResultStorage.unknownFilter["saveCsvMode"] != 0:
            unknownCsv.create_csv()

        confid = confidence.cpu().numpy()
        for i in range(len(predict)):
            score = confid[i, predict[i]] if not reverse else -1*confid[i, predict[i]]
            fullname = nameList[count]
            result = []
            for tagName, threshold in filter:
                if reverse:  threshold = -1*threshold 
                if mode == "Test":
                    if  score < threshold: 
                        print(f'{tagName} file: {fullname}, Label: {className[int(labels[i])]}',
                            f'sorce({score:.2f}) < threshold({threshold})' if not reverse else f'sorce({score*-1:.2f}) > threshold({threshold*-1})')
                        result = [fullname, className[int(labels[i])], tagName, f'{score if not reverse else score*-1:.2f}']
                        break  
                    elif ResultStorage.unknownFilter["saveCsvMode"] == 2:
                        result =  [fullname, className[int(labels[i])], className[int(predict[i])], f'{score if not reverse else score*-1:.2f}']
        
                else:
                    if score < threshold: 
                        print(f'{tagName} file: {fullname}',
                            f'sorce({score:.2f}) < threshold({threshold})' if not reverse else f'sorce({score*-1:.2f}) > threshold({threshold*-1})')
                        result = [fullname, tagName, f'{score if not reverse else score*-1:.2f}']  
                        break
                    elif ResultStorage.unknownFilter["saveCsvMode"] == 2:
                        result = [fullname, className[int(predict[i])], f'{score if not reverse else score*-1:.2f}']
            if len(result) != 0: unknownCsv.writing(result, 'a')                     
            count += 1
    return count
