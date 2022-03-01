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
    transformList = [transforms.Resize((PreprocessPara.imageSize[0], PreprocessPara.imageSize[1]))]
    
    if AugmentationPara.randomHorizontalFlip['switch']:
        transformList.append(transforms.RandomHorizontalFlip(p=AugmentationPara.randomHorizontalFlip['probability']))
    
    if AugmentationPara.randomVerticalFlip['switch']:
        transformList.append(transforms.RandomVerticalFlip(p=AugmentationPara.randomHorizontalFlip['probability']))
    
    if PreprocessPara.normalize['switch']:
        set_normalize(transformList)
    else:
        transformList.append(transforms.ToTensor())
    
    dataTransforms = transforms.Compose(transformList)
    return dataTransforms


def select_transform():
    transformList = [transforms.Resize((PreprocessPara.imageSize[0], PreprocessPara.imageSize[1]))]
    if PreprocessPara.normalize['switch']:
        if PreprocessPara.normalize['mode'] == 3:
            raise BaseException("In Test or Inference task, the normalization value should't be calculated by dataset.")
        else:
            set_normalize(transformList)
    else:
        transformList.append(transforms.ToTensor())

    dataTransforms = transforms.Compose(transformList)
    return dataTransforms



def set_normalize(transformList):
    transformList.append(transforms.ToTensor())

    # ImageNet
    if PreprocessPara.normalize['mode'] == 0:
        transformList.append(transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)))
    
    # CIFAR10
    elif PreprocessPara.normalize['mode'] == 1:
        transformList.append(transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)))

    # MNIST
    elif PreprocessPara.normalize['mode'] == 2:
        transformList.append(transforms.Normalize((0.1307, 0.1307, 0.1307), (0.3801, 0.3801, 0.3801)))
    
    # Calculate data mean and std
    elif PreprocessPara.normalize['mode'] == 3:
        mean, std = NormalizeValueCalculate.get_std_mean(PreprocessPara.imageSize)
        transformList.append(transforms.Normalize((mean[0].item(), mean[1].item(), mean[2].item()), (std[0].item(), std[1].item(), std[2].item())))
    
    # Take user input
    elif PreprocessPara.normalize['mode'] == 4:
        transformList.append(transforms.Normalize((PreprocessPara.normalize['mean']), (PreprocessPara.normalize['std'])))
    
    else:
        raise BaseException("(Preprocess Config error) Please select correct normalize mode.(0, 1, 2, 3, 4)")
