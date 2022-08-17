# -*- coding: utf-8 -*-

"""
Created on Tue Jul 05 12:00:00 2022
"""

import os
from config.Config import PrivateSetting, BasicSetting
from config.ConfigPytorchModel import ClsPath
from config.ConfigPostprocess import PostProcessPara
from utils.ModelService.PytorchClassificationModel import MainProcess
from utils.Postprocess import SetPostprocess
from utils.Evaluation import SelectEvaluationMethod
from utils.ResultStorage import SelectStorageMethod

def train():
    '''
    Call training module
    '''
    print("Step 0: AI model Training")
    MainProcess.train()
    print("Step 1: Generating ini")
    classNameList = []  
    for folder in os.listdir(ClsPath.trainPath):
        if os.path.isdir(os.path.join(ClsPath.trainPath, folder)):
            classNameList.append(folder)
    SelectStorageMethod.save_ini_file(PrivateSetting.outputPath, classNameList, PostProcessPara.unknownFilter)

def test():
    '''
    Call testing module
    '''
    print("Step 0: AI model Testing")
    resultList = MainProcess.test()
    print("Step 1: Post-processing")
    resultList = SetPostprocess.select_postprocess(resultList)
    print("Step 2: Evaluating")
    classNameList = []  
    for folder in os.listdir(ClsPath.testPath):
        if os.path.isdir(os.path.join(ClsPath.testPath, folder)):
            classNameList.append(folder)
    SelectEvaluationMethod.test_evaluation(resultList, classNameList)
    print("Step 3: Result Saveing")
    SelectStorageMethod.save_result(resultList, classNameList, PrivateSetting.outputPath, BasicSetting.task)
    
def inference():
    '''
    Call inference module
    '''
    print("Step 0: AI model Inference")
    resultList = MainProcess.inference()
    print("Step 1: Post-processing")
    resultList = SetPostprocess.select_postprocess(resultList)
    print("Step 2: Result Saveing")
    SelectStorageMethod.save_result(resultList, BasicSetting.classNameList, PrivateSetting.outputPath, BasicSetting.task)

def model_main():
    '''
    根據config中的task, 選擇對應程式執行
    '''
    print(f"......... Project: {BasicSetting.projectName}, Experiment: {BasicSetting.runId}, Mode: {BasicSetting.task} .........")
    try:
        if BasicSetting.task == 'Train':
            train()
        elif BasicSetting.task == 'Test':
            test()
        elif BasicSetting.task == 'Inference':
            inference()
        elif BasicSetting.task == 'Retrain':
            train()
        else:
            raise BaseException("Please set up the correct task mode")
        return True
    except Exception as err:
        print(err)
        return False

if __name__ == "__main__":
    model_main()