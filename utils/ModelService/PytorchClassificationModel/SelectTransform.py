# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""
from PIL import Image
from torchvision import transforms
from config.ConfigPreprocess import PreprocessPara
from config.ConfigAugmentation import AugmentationPara as augPara
from utils.Preprocess import NormalizeValueCalculate

def preprocess_transform():
    """
    set preprocess transform: according to ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: preprocess transform
    """
    preTransformList = []
    if PreprocessPara.resize["switch"]:
        preTransformList.append(transforms.Resize(size=PreprocessPara.resize["imageSize"], interpolation=getattr(Image, augPara.randomPerspective["interpolation"])))

    if PreprocessPara.centerCrop["switch"]:
        preTransformList.append(transforms.CenterCrop(PreprocessPara.centerCrop["size"]))        
    
    if PreprocessPara.pad["switch"]:
        preTransformList.append(transforms.Pad(PreprocessPara.pad["padding"], PreprocessPara.pad["fill"], PreprocessPara.pad["paddingModel"]))

    if PreprocessPara.gaussianBlur["switch"]:
        preTransformList.append(transforms.GaussianBlur(PreprocessPara.gaussianBlur["kernelSize"], PreprocessPara.gaussianBlur["sigma"]))

    if PreprocessPara.brightness["switch"]:
        preTransformList.append(transforms.ColorJitter(brightness=[PreprocessPara.brightness["brightness"], PreprocessPara.brightness["brightness"]]))

    if PreprocessPara.contrast["switch"]:
        preTransformList.append(transforms.ColorJitter(contrast=[PreprocessPara.contrast["contrast"], PreprocessPara.contrast["contrast"]]))

    if PreprocessPara.saturation["switch"]:
        preTransformList.append(transforms.ColorJitter(saturation=[PreprocessPara.saturation["saturation"], PreprocessPara.saturation["saturation"]]))

    if PreprocessPara.hue["switch"]:
        preTransformList.append(transforms.ColorJitter(hue=[PreprocessPara.hue["hue"], PreprocessPara.hue["hue"]]))
        
    return preTransformList


def augmentation_transform(augTransformList):
    """
    set augmentation transform: according to ConfigAugmentation, setting augmentation module.

    Return:
        dataTransforms: augmentation transform
    """
    if augPara.randomHorizontalFlip["switch"]:
        augTransformList.append(transforms.RandomHorizontalFlip(p=augPara.randomHorizontalFlip["probability"]))
    
    if augPara.randomVerticalFlip["switch"]:
        augTransformList.append(transforms.RandomVerticalFlip(p=augPara.randomHorizontalFlip["probability"]))
    
    if augPara.randomRotation["switch"]:
        augTransformList.append(transforms.RandomAffine(degrees=augPara.randomRotation["degress"]))

    if augPara.randomTranslate["switch"]:
        augTransformList.append(transforms.RandomAffine(degrees=0, translate=augPara.randomTranslate["translate"]))

    if augPara.randomScale["switch"]:
        augTransformList.append(transforms.RandomAffine(degrees=0, scale=augPara.randomScale["scale"]))

    if augPara.randomShear["switch"]:
        augTransformList.append(transforms.RandomAffine(degrees=0, shear=augPara.randomShear["shear"]))
    
    if augPara.randomGrayscale["switch"]:
        augTransformList.append(transforms.RandomGrayscale(p=augPara.randomGrayscale["probability"]))

    if augPara.randomBrightness["switch"]:
        augTransformList.append(transforms.ColorJitter(brightness=augPara.randomBrightness["brightness"]))

    if augPara.randomContrast["switch"]:
        augTransformList.append(transforms.ColorJitter(contrast=augPara.randomContrast["contrast"]))

    if augPara.randomSaturation["switch"]:
        augTransformList.append(transforms.ColorJitter(saturation=augPara.randomSaturation["saturation"]))

    if augPara.randomHue["switch"]:
        augTransformList.append(transforms.ColorJitter(hue=augPara.randomHue["hue"]))
    
    # if augPara.randomPosterize["switch"]:
    #     augTransformList.append(transforms.RandomPosterize(bits=augPara.randomPosterize["bits"],
    #                                                     p=augPara.randomPosterize["probability"]))
    
    # if augPara.randomSolarize["switch"]:
    #     augTransformList.append(transforms.RandomSolarize(threshold=augPara.randomSolarize["threshold"],
    #                                                    p=augPara.randomSolarize["probability"]))

    # if augPara.randomAdjustSharpness["switch"]:
    #     augTransformList.append(transforms.RandomAdjustSharpness(sharpness_factor=augPara.randomAdjustSharpness["sharpness"],
    #                                                           p=augPara.randomAdjustSharpness["probability"]))

    # if augPara.randomAutocontrast["switch"]:
    #     augTransformList.append(transforms.RandomAutocontrast(p=augPara.randomAutocontrast["probability"]))

    if augPara.randomPerspective["switch"]:       
        augTransformList.append(transforms.RandomPerspective(distortion_scale=augPara.randomPerspective["distortion"],
                                                             p=augPara.randomPerspective["probability"],
                                                             interpolation=getattr(Image, augPara.randomPerspective["interpolation"])))

    if PreprocessPara.normalize["switch"]:
        normalization = set_normalize(augTransformList)
    else:
        normalization = None
        augTransformList.append(transforms.ToTensor())
    
    if augPara.randomErasing["switch"]:
        valueRGB = [x / 255 for x in augPara.randomErasing["value"]]
        augTransformList.append(transforms.RandomErasing(p=augPara.randomErasing["probability"],
                                                         scale=augPara.randomErasing["scale"],
                                                         ratio=augPara.randomErasing["ratio"],
                                                         value=valueRGB))
    return augTransformList, normalization

def set_normalize(transformList):
    """
    Add transforms.ToTensor() and according to PreprocessPara.normalize in ConfigPreprocess, setting normalized value.
    """
    transformList.append(transforms.ToTensor())

    # ImageNet
    if PreprocessPara.normalize["mode"] == 0:
        normalization = {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}
    
    # CIFAR10
    elif PreprocessPara.normalize["mode"] == 1:
        normalization = {"mean": [0.4914, 0.4822, 0.4465], "std": [0.2023, 0.1994, 0.2010]}

    # MNIST
    elif PreprocessPara.normalize["mode"] == 2:
        normalization = {"mean": [0.1307, 0.1307, 0.1307], "std": [0.3801, 0.3801, 0.3801]}
    
    # Calculate data mean and std
    elif PreprocessPara.normalize["mode"] == 3:
        mean, std = NormalizeValueCalculate.get_std_mean(PreprocessPara.resize["imageSize"])
        normalization = {"mean": mean, "std": std}
        
    # Take user input
    elif PreprocessPara.normalize["mode"] == 4:
        normalization = {"mean": PreprocessPara.normalize["mean"], "std": PreprocessPara.normalize["std"]}
    
    # ABF
    elif PreprocessPara.normalize["mode"] == 5:
        normalization = {"mean": [0.49002929, 0.49002929, 0.49002929], "std": [0.26184613, 0.26184613, 0.26184613]}

    # VRS
    elif PreprocessPara.normalize["mode"] == 6:
        normalization = {"mean": [0.72043937, 0.72043937, 0.72043937], "std": [0.3669707, 0.3669707, 0.3669707]}
    
    else:
        raise BaseException("(Preprocess Config error) Please select correct normalize mode.(0, 1, 2, 3, 4, 5, 6)")
    
    transformList.append(transforms.Normalize(normalization["mean"], normalization["std"]))

    return normalization


def select_train_transform():
    """
    Set train transform: according to ConfigAugmentation and ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: train transform
    """
    transformList = preprocess_transform()
    transformList, normalization = augmentation_transform(transformList)

    dataTransforms = transforms.Compose(transformList)
    return dataTransforms, normalization


def select_valid_transform(normalization):
    """
    Set validation transform: according to ConfigAugmentation and ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: test or inference transform
    """
    transformList = preprocess_transform()

    transformList.append(transforms.ToTensor())
    
    if PreprocessPara.normalize["switch"]:       
        transformList.append(transforms.Normalize(normalization["mean"], normalization["std"]))

    dataTransforms = transforms.Compose(transformList)
    return dataTransforms


def select_transform():
    """
    Set test or inference transform: according to ConfigAugmentation and ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: test or inference transform
    """
    transformList = preprocess_transform()
   
    if PreprocessPara.normalize["switch"]:
        if PreprocessPara.normalize["mode"] == 3:
            raise BaseException('In Test or Inference task, the normalization value should not be calculated by dataset.\nPlease choose other normalize["mode"] in ./config/ConfigPreprocess.')
        else:
            _ = set_normalize(transformList)
    else:
        transformList.append(transforms.ToTensor())

    dataTransforms = transforms.Compose(transformList)
    return dataTransforms


    # Preprocess

    # Aug (Totensor)

    # Normalize (Totensor)

    # Totensor