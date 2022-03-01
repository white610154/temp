# -*- coding: utf-8 -*-

"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""

import os, shutil
from distutils.dir_util import copy_tree
from PIL import Image


def get_specific_files(filePath, fileType):
    """
    回傳指定路徑下，符合特定副檔名或檔案類型的檔名列表

    Args:
        filePath: 指定路徑
        fileType: 指定資料類型: 'image', '.txt'
    """
    finalList = []
    if fileType == 'image':
        for name in os.listdir(filePath):
            try:
                Image.open(os.path.join(filePath, name))
                finalList.append(name)
            except:
                continue
    else:
        for file in os.listdir(filePath):
            if file.endswith(fileType):
                finalList.append(file)
    return finalList


def copy_files_in_list(imageList, dataPath, folderName):
    """
    依照給定的檔名列表，將資料複製到目的地路徑下

    Args:
        imageList: 檔名列表
        dataPath: 資料來源的資料夾
        folderName: 目的地路徑
    """
    create_empty_folder(folderName)
    
    for imgName in imageList:
        shutil.copy(os.path.join(dataPath, imgName), folderName)


def copy_all_files(origPath, outputPath):
    """
    將來源地資料夾下所有東西複製到目標位置，目標位置若已存在會被完全取代
    
    Args:
        origPath: 來源地資料夾(必須是資料夾)
        outputPath: 目標位置
    """
    resultPath = os.path.join(outputPath, origPath.split('/')[-1])
    create_empty_folder(resultPath)

    if os.path.isfile(origPath):
        raise BaseException("(State error) Please place the file in to a folder.")
        shutil.copy(origPath, outputPath)

    elif os.path.isdir(origPath):
        copy_tree(origPath, resultPath)


def delete_files(filePath):
    """
    刪除指定路徑下的檔案或資料夾
    """
    if os.path.isdir(filePath): shutil.rmtree(filePath)
    elif os.path.isfile(filePath): os.remove(filePath)
    else: pass
    

def create_empty_folder(folderPath):
    """
    建立指定的空資料夾，若同名資料夾已存在則會刪除舊的，建立新的
    """
    if os.path.isdir(folderPath): shutil.rmtree(folderPath)
    os.makedirs(folderPath)
