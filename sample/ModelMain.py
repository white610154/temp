# -*- coding: utf-8 -*-

"""
Created on TUE Dec 7 20:00:00 2021
@author: OtisChang
"""
from config.Config import BasicSetting
from utils.ModelService.PytorchClassificationModel import MainProcess

def train():
    '''
    Call training module
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
    Call testing module
    '''
    MainProcess.test()
    

def inference():
    '''
    Call inference module
    '''
    MainProcess.inference()


def model_main():
    print(f"========== Project: {BasicSetting.projectName}, Run:{BasicSetting.runId}, Mode:{BasicSetting.task} ==========")
    
    if BasicSetting.task == 'Train':
        train()
    elif BasicSetting.task == 'Test':
        test()
    elif BasicSetting.task == 'Inference':
        inference()
    else:
        raise BaseException("Please set up the correct task mode in config/Config.py.")
