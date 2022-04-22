# -*- coding: utf-8 -*-

"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""

import os
from utils.DatasetClean.BasicFileProcess import *


def copy_user_input(outputPath, state, imagePath, annotationPath, **kwargs):
    """
    依照使用者輸入的資料狀態將檔案複製到outputPath，並刪除舊有資料
    
    Args:
        outputPath: 檔案複製的位置
        state: 要複製的檔案狀態(0: 全部影像+YOLO標記檔, 1: 依類別分好的影像資料夾, 2: 已分好資料集的資料夾)
        imagePath: 影像或是資料夾的路徑
        labelPath: 標記檔路徑
    return:
        複製資料及label的目的地路徑
    """
    dataPath = os.path.join(outputPath, imagePath.split('/')[-1])
    delete_files(dataPath)

    if state == 0:
        imgList = get_specific_files(imagePath, 'image')
        copy_files_in_list(imgList, imagePath, os.path.join(outputPath, imagePath.split('/')[-1]))
        labelList = get_specific_files(annotationPath, '.txt')
        copy_files_in_list(labelList, annotationPath, os.path.join(outputPath, annotationPath.split('/')[-1]))
        
        labelPath = os.path.join(outputPath, annotationPath.split('/')[-1])

    elif state == 1 or state == 2:
        for folder in os.listdir(imagePath):
            try:
                fileList = get_specific_files(os.path.join(imagePath, folder), 'image')
            except:
                raise BaseException(f"(State error) The data structure and DATA_STATE[state] setting must be consistent.")
            copy_files_in_list(fileList, os.path.join(imagePath, folder), os.path.join(outputPath, imagePath.split('/')[-1], folder))
        
        labelPath = None
    
    else:
        raise BaseException("(Config error) DATA_STATE[state] must be 0, 1, or 2.")

    return dataPath, labelPath