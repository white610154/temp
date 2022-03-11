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
    model              = {'structure': 'se_cbam_resnext50_32x4d', 'pretrained': False}


### Set up model parameters  ###
class ClsModelPara:
    cudaDevice         = 2   # GPU device used for running program
    batchSize          = 32   # Number of data use for training at the same time
    epochs             = 20   # The iteration number of training


### Set up path  ###
class ClsPath:
    ### Data path
    trainPath          = "./input/Data/seven_type_ok_mmfa/Train"     # Train data path
    validPath          = "./input/Data/seven_type_ok_mmfa/Valid"     # Validation data path
    testPath           = "./input/Data/seven_type_ok_mmfa/Test"           # Test data path
    inferencePath      = "./input/Data/Dimple"             # Inference data path
    
    ### Weight path
    pretrainedWeight   = f"./input/PretrainedWeight/{SelectedModel.model['structure']}.pth" # Model weight for training
    weightPath         = f'./{PrivateSetting.outputPath}/BestWeight.pth'                    # Model weight for test and inference