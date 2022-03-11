# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""
"""
The function of DataClean package haven't completely developed.
"""
class DataSetting:
    # state: Input file state(0: all images + YOLO annotation files, 1: images have placed in each class folders, 2: the dataset folders have ready) ； 
    # imagePath: image path ； labelPath: annotation file path ； Annotation: annotation type(YOLO, PascalVOC)
    dataState    = {"state": 0, "imagePath": './input/Image',
                    "annotationPath": './input/Label', "annotationType": 'YOLO'}
    dataSplitPercentage   = [0.8, 0.1, 0.1] # [train, valid, test]
    cropImage    = False                    # If images need to crop or not.

