# -*- coding: utf-8 -*-

"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""

from torchvision import transforms
from config.ConfigPreprocess import PreprocessPara
from config.ConfigAugmentation import AugmentationPara
from utils.Preprocess import NormalizeValueCalculate

def select_train_transform():
    """
    Set train transform: according to ConfigAugmentation and ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: train transform
    """
    mean, std = [], []
    transformList = [transforms.Resize((PreprocessPara.imageSize[0], PreprocessPara.imageSize[1]))]
    
    if AugmentationPara.randomHorizontalFlip['switch']:
        transformList.append(transforms.RandomHorizontalFlip(p=AugmentationPara.randomHorizontalFlip['probability']))
    
    if AugmentationPara.randomVerticalFlip['switch']:
        transformList.append(transforms.RandomVerticalFlip(p=AugmentationPara.randomHorizontalFlip['probability']))
    
    if PreprocessPara.normalize['switch']:
        mean, std = set_normalize(transformList)
    else:
        transformList.append(transforms.ToTensor())
    
    dataTransforms = transforms.Compose(transformList)
    return dataTransforms, mean, std


def select_valid_transform(mean, std):
    """
    Set validation transform: according to ConfigAugmentation and ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: test or inference transform
    """
    transformList = [transforms.Resize((PreprocessPara.imageSize[0], PreprocessPara.imageSize[1]))]
    if PreprocessPara.normalize['switch']:
        transformList.append(transforms.ToTensor())
        transformList.append(transforms.Normalize(mean, std))
    else:
        transformList.append(transforms.ToTensor())

    dataTransforms = transforms.Compose(transformList)
    return dataTransforms


def select_transform():
    """
    Set test or inference transform: according to ConfigAugmentation and ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: test or inference transform
    """
    transformList = [transforms.Resize((PreprocessPara.imageSize[0], PreprocessPara.imageSize[1]))]
    if PreprocessPara.normalize['switch']:
        if PreprocessPara.normalize['mode'] == 3:
            raise BaseException("In Test or Inference task, the normalization value should't be calculated by dataset.\nPlease choose other normalize['mode'] in ./config/ConfigPreprocess.")
        else:
            _, _ = set_normalize(transformList)
    else:
        transformList.append(transforms.ToTensor())

    dataTransforms = transforms.Compose(transformList)
    return dataTransforms



def set_normalize(transformList):
    """
    Add transforms.ToTensor() and according to PreprocessPara.normalize in ConfigPreprocess, setting normalized value.
    """
    transformList.append(transforms.ToTensor())
    mean, std = [], []

    # ImageNet
    if PreprocessPara.normalize['mode'] == 0:
        mean, std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    
    # CIFAR10
    elif PreprocessPara.normalize['mode'] == 1:
        mean, std = [0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010]

    # MNIST
    elif PreprocessPara.normalize['mode'] == 2:
        mean, std = [0.1307, 0.1307, 0.1307], [0.3801, 0.3801, 0.3801]
    
    # Calculate data mean and std
    elif PreprocessPara.normalize['mode'] == 3:
        mean, std = NormalizeValueCalculate.get_std_mean(PreprocessPara.imageSize)
        
    # Take user input
    elif PreprocessPara.normalize['mode'] == 4:
        mean, std = PreprocessPara.normalize['mean'], PreprocessPara.normalize['std']
    
    # ABF
    elif PreprocessPara.normalize['mode'] == 5:
        mean, std = [0.49002929, 0.49002929, 0.49002929], [0.26184613, 0.26184613, 0.26184613]

    # VRS
    elif PreprocessPara.normalize['mode'] == 6:
        mean, std = [0.72043937, 0.72043937, 0.72043937], [0.3669707, 0.3669707, 0.3669707]
    
    else:
        raise BaseException("(Preprocess Config error) Please select correct normalize mode.(0, 1, 2, 3, 4)")
    
    transformList.append(transforms.Normalize(mean, std))

    return mean, std