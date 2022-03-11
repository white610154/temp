# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""
from config.Config import PrivateSetting

### Select your model ###
class SelectedModel:
    """
    The model including: AlexNet, DenseNet, EfficientNet, MnasNet, MobileNetV3, RegNet, ResNet
                         ShuffleNetV2, VGG, cbam_resnet, se_cbam_resnet, se_resnet
    For the detail structure name, please check out each code in ./utils/AiModel package.
    """
    model              = {'structure': 'regnet_y_400mf', 'pretrained': True}


### Set up model parameters  ###
class ClsModelPara:
    cudaDevice         = 2   # GPU device used for running program
    batchSize          = 32   # Number of data use for training at the same time
    epochs             = 20   # The iteration number of training


### Set up path  ###
class ClsPath:
    ### Data path
    trainPath          = ""     # Train data path
    validPath          = ""     # Validation data path
    testPath           = ""           # Test data path
    inferencePath      = ""             # Inference data path
    
    ### Weight path
    pretrainedWeight   = f"./input/PretrainedWeight/{SelectedModel.model['structure']}.pth" # Model weight for training
    weightPath         = f'./{PrivateSetting.outputPath}/BestWeight.pth'                    # Model weight for test and inference