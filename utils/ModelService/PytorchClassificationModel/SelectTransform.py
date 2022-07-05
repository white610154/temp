# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""

from PIL import Image
from torchvision import transforms
from config.ConfigPreprocess import PreprocessPara
from config.ConfigAugmentation import AugmentationPara as augPara

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
        preTransformList.append(transforms.Pad(PreprocessPara.pad["padding"], tuple(PreprocessPara.pad["fill"]), PreprocessPara.pad["paddingMode"]))

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


def augmentation_transform(augTransformList, normalizedValue=None):
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
        augTransformList.append(transforms.RandomAffine(degrees=augPara.randomRotation["degress"], 
                                                        fillcolor=tuple(augPara.randomRotation["fill"])))

    if augPara.randomTranslate["switch"]:
        augTransformList.append(transforms.RandomAffine(degrees=0, 
                                                        translate=augPara.randomTranslate["translate"],
                                                        fillcolor=tuple(augPara.randomRotation["fill"])))

    if augPara.randomScale["switch"]:
        augTransformList.append(transforms.RandomAffine(degrees=0, 
                                                        scale=augPara.randomScale["scale"],
                                                        fillcolor=tuple(augPara.randomRotation["fill"])))

    if augPara.randomShear["switch"]:
        augTransformList.append(transforms.RandomAffine(degrees=0, 
                                                        shear=augPara.randomShear["shear"],
                                                        fillcolor=tuple(augPara.randomRotation["fill"])))
    
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
                                                             interpolation=getattr(Image, augPara.randomPerspective["interpolation"]),
                                                             fill=tuple(augPara.randomPerspective["fill"])))

    augTransformList.append(transforms.ToTensor())
    if PreprocessPara.normalize["switch"]:
        augTransformList.append(transforms.Normalize(normalizedValue["mean"], normalizedValue["std"]))
    
    if augPara.randomErasing["switch"]:
        valueRGB = [x / 255 for x in augPara.randomErasing["value"]]
        augTransformList.append(transforms.RandomErasing(p=augPara.randomErasing["probability"],
                                                         scale=augPara.randomErasing["scale"],
                                                         ratio=augPara.randomErasing["ratio"],
                                                         value=valueRGB))
    return augTransformList, normalizedValue


def select_train_transform(normalizedValue):
    """
    Set train transform: according to ConfigAugmentation and ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: train transform
    """
    transformList = preprocess_transform()
    transformList, normalizedValue = augmentation_transform(transformList, normalizedValue)

    dataTransforms = transforms.Compose(transformList)
    return dataTransforms


def select_valid_transform(normalizedValue):
    """
    Set validation transform: according to ConfigAugmentation and ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: test or inference transform
    """
    transformList = preprocess_transform()
    transformList.append(transforms.ToTensor())
    if PreprocessPara.normalize["switch"]:
        transformList.append(transforms.Normalize(normalizedValue["mean"], normalizedValue["std"]))   

    dataTransforms = transforms.Compose(transformList)
    return dataTransforms


def select_transform(normalizedValue):
    """
    Set test or inference transform: according to ConfigAugmentation and ConfigPreprocess, setting transform module.

    Return:
        dataTransforms: test or inference transform
    """
    transformList = preprocess_transform()
    transformList.append(transforms.ToTensor())
    if PreprocessPara.normalize["switch"]:
        transformList.append(transforms.Normalize(normalizedValue["mean"], normalizedValue["std"]))

    dataTransforms = transforms.Compose(transformList)
    return dataTransforms