# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""
from config.Config import BasicSetting, PrivateSetting

class DataSetting:
    # state: 檔案狀態(0: 全部影像+YOLO標記檔, 1: 依類別分好的影像資料夾, 2: 已分好資料集的資料夾) ； 
    # imagePath: 影像路徑 ； labelPath: 標記檔路徑 ； Annotation: 標記檔格式(YOLO, PascalVOC)
    # state = 0: 圖片和標記txt檔各一個資料夾，檔名對應
    # state = 1: 圖片依照類別分好資料夾，但尚未切分資料集
    # state = 2: 圖片已分好資料集，資料集下含各類別資料夾
    dataState    = {"state": 0, "imagePath": './input/Image',
                    "annotationPath": './input/Label', "annotationType": 'YOLO'}
    dataSplitPercentage   = [0.8, 0.1, 0.1] # [train, valid, test]
    cropImage    = False
    className    = ['1', '2', '3', '4', '5', '6']
