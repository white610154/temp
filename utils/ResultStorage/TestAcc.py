import os, csv, json
from torch import tensor
from config.Config import BasicSetting, PrivateSetting
from config.ConfigResultStorage import ResultStorage

def test_epoch_acc_json(classTotal:list, classCorrect:list):
    """
    Save epoch accuracy and class accuracy into json file.

    Args:
        classTotal: data amount of each class
        classCorrect: correctly predicted data amount of each class
    Return:
        modelTesting.json
    """
    jsonFilePath = f'./{PrivateSetting.outputPath}/modelTesting.json'
    epochDict = {
        "test": {
            "accuracy": sum(classCorrect) / sum(classTotal)
        }
    }
    infoDict = {}
    infoDict["test"] = epochDict
    with open(jsonFilePath, 'w') as fAcc:
        json.dump(infoDict, fAcc, indent=4)