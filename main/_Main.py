# -*- coding: utf-8 -*-

"""
Created on TUE Dec 7 20:00:00 2021
@author: OtisChang
"""
from config.Config import BasicSetting, PrivateSetting
from utils.DatasetClean import CopyUserInput, DataSplit, CropImage
from utils.ModelService.PytorchClassificationModel import MainProcess

def train():
    '''
    讀入PROJECT_ID, EXPERIMENT_ID
    進行本次實驗模型、前處理、後處理查找
    '''
    # print("Step 1: Dataset Split")
    # dataPath, labelPath = CopyUserInput.copy_user_input(PrivateSetting.DATASET_PATH, **DataSetting.DATA_STATE)
    # DataSplit.data_split(dataPath, labelPath)

    # print("Step 2: Image Cropping")
    # CropImage.CropTrain(dataPath, labelPath, **DataSetting.DATA_STATE)

    # 這兩個項目用transforms做，但還是提供外部模組
    # print("- Step 3: Data Augmentation")
    # print("- Step 4: Preprocessing")

    print("Step 0: AI model Training")
    MainProcess.train()

    # print("Step 6: Delete dataset")

def test():
    '''
    讀入ProjectID = 1; ExperimentID = 1
    進行本次實驗模型、前處理、後處理查找
    '''
    MainProcess.test()
    

def inference():
    '''
    讀入ProjectID = 1; ExperimentID = 1
    進行本次實驗模型、前處理、後處理查找
    '''
    MainProcess.inference()


def main():
    print(f"========== Project: {BasicSetting.projectID}, Experiment:{BasicSetting.experimentID}, Mode:{BasicSetting.task} ==========")
    
    if BasicSetting.task == 'Train':
        train()
    elif BasicSetting.task == 'Test':
        test()
    elif BasicSetting.task == 'Inference':
        inference()
    else:
        print("請於 config/Config.py 中設定 TASK 模式")
        exit()
