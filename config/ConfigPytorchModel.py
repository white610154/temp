# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""
from config.Config import PrivateSetting

##### 模型選擇 #####
class SelectedModel:
    # resnext50_32x4d, regnet_y_400mf, ....
    model              = {'structure': 'regnet_y_400mf', 'pretrained': True}


##### 模型參數設定 #####
class ClsModelPara:
    cudaDevice         = 1
    batchSize          = 8
    epochs             = 2


##### 相關路徑設定 #####
class ClsPath:
    ### 資料路徑 ###
    trainPath          = './input/Data/ten_type/Train'
    validPath          = './input/Data/ten_type/Valid'
    testPath           = './input/Data/ten_type/Test'
    inferencePath      = './input/Data/ten_type/Inference'
    
    ### 權重路徑 ###
    pretrainedWeight   = f"./input/PretrainedWeight/{SelectedModel.model['structure']}.pth"
    weightPath         = f'./{PrivateSetting.outputPath}/BestWeight.pth'