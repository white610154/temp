# -*- coding: utf-8 -*-

"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""

import os, shutil, math
from shutil import copyfile
from sklearn.model_selection import train_test_split

from utils.DatasetClean.BasicFileProcess import *
from config.Config import PrivateSetting
from config.ConfigDataClean import DataSetting

"""
state: 使用者input的資料狀態
datasetPath: 切分資料集後的根目錄
percentage: [train, valid, test]資料集切分的比例，三個值不小於0且相加需等於1
"""
state = DataSetting.dataState["state"]
datasetPath = PrivateSetting.datasetPath
percentage = DataSetting.dataSplitPercentage

def data_split(dataPath, labelPath):
    """
    若state等於0或1，便會根據設定的比例切分Train、Valid、Test三個資料集
    若state等於2，則表示資料集已切分完成，無須再切分
    最終於結果路徑下產生三個資料夾: Train、Valid、Test
    """
    setList = ['Train', 'Valid', 'Test']
    folderNames = [None, None, None]
    for i, folderName in enumerate(setList):
        folderNames[i] = os.path.join(datasetPath, folderName)

    if state == 0:
        datasetList = split_dataset(imgPath=dataPath, annotationPath=labelPath)
        for i, folderName in enumerate(folderNames):
            copy_files_in_list(datasetList[i], dataPath, folderName)
        delete_files(dataPath)

    elif state == 1:
        classes = os.listdir(dataPath)
        for className in classes:
            datasetList = split_dataset(imgPath=os.path.join(dataPath, className), className=className)
            for i, folderName in enumerate(folderNames):
                copy_files_in_list(datasetList[i], os.path.join(dataPath, className), os.path.join(folderName, className))
        delete_files(dataPath)
    
    elif state == 2:
        for datasetName in setList:
            if datasetName not in os.listdir(dataPath):
                raise BaseException("(State error) The dataset(folder name) must include 'Train', 'Valid', and 'Test'.")
        for i, folderName in enumerate(folderNames):
            copy_all_files(dataPath, folderName)



def split_dataset(imgPath, annotationPath=None, percentage=percentage, className=None):
    """
    根據給定的資料路徑以及比例切分出train、valid、test資料集名稱的列表

    Args:
        imgPath: 資料路徑
        annotationPath: 標記檔路徑
        percentage: 比例值[train, valid, test]
        className: dataPath下若還有資料夾名稱，須給資料夾名稱
    return:
        三個資料集的檔名列表
    """
    if sum(percentage) != 1:
        raise BaseException("(Config error) The sum of percentage must be 1")

    imgList = get_specific_files(imgPath, 'image')
    for rate in percentage:
        if len(imgList) * rate < 1:
            if className != None:
                print(f" - The data amount in {className} are less than 10. Duplicate the images to avoid some dataset has no data.")
                imgList = duplicate_file(imgPath=imgPath, className=className)
            else:
                print(" - The data amount are less than 10. Duplicate the images to avoid some dataset has no data.")
                imgList = duplicate_file(imgPath=imgPath, annotationPath=annotationPath)
    
    trainImages, validNTestImages = train_test_split(imgList, test_size=sum(percentage[1:3]), random_state=233)
    validImages, testImages = train_test_split(validNTestImages, test_size=percentage[2]/sum(percentage[1:3]), random_state=233)
    datasetList = [trainImages, validImages, testImages]      
    
    return datasetList



def duplicate_file(imgPath, annotationPath=None, className=None, targetNum=10):
    """
    若資料夾下的資料數量不足目標數量，則進行複製直到滿足目標數量

    Args:
        targetNum: 目標數量
        imgPath: 欲增加資料的資料夾路徑
        annotationPath: 若有對應的標註檔，則須給標註檔路徑
        className: dataPath下若有再分類別資料夾，須給資料夾名稱
    return:
        完成複製後的資料檔名列表
    """
    if len(os.listdir(imgPath)) == 0:
        if className != None:
            raise BaseException(f"(State error) Please delete the empty folder {className}")
        else:
            raise BaseException(f"(State error) Please delete the empty folder or check DATA_STATE[state].")
    else:
        ### Copy image
        copyIter = int(math.ceil(targetNum - len(os.listdir(imgPath))) / len(os.listdir(imgPath)))
        copyImgList = os.listdir(imgPath)
        for i in range(copyIter):
            for file in copyImgList:
                copyfile(os.path.join(imgPath, file), os.path.join(imgPath, f'clone{i}_{file}'))
        
        ### Copy label
        if className == None:
            copyLabelList = os.listdir(annotationPath)
            if len(copyImgList) != len(copyLabelList):
                raise BaseException(f"(State error) The amount of data doesn't match the amount of label files")
            else:
                copyIter = int(math.ceil(targetNum - len(copyLabelList)) / len(copyLabelList))
                for i in range(copyIter):
                    for file in copyLabelList:
                        copyfile(os.path.join(annotationPath, file), os.path.join(annotationPath, f'clone{i}_{file}'))

    return os.listdir(imgPath)



def split_dataset_by_txt(txt_path:str, raw_data_path:str, output_path:str, dataset:list):
    """
    依照txt_path下test, train, valid三個txt檔中的檔名列表切分檔案到三個資料夾下

    Args:
        txt_path: txt檔的路徑，下含三個txt檔[train, test, valid]
        raw_data_path: 原始所有影像的路徑
        output_path: 輸出切分結果的路徑
        dataset: 要切分的資料集種類，與txt檔數量相同[train, test, valid]

    Return:
        dataset_path: 各資料集資料夾的路徑，下含要切defect的原始圖片
    """
    print("- dataset dividing ...")

    dataset_path = []
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    for i in range(len(dataset)):
        if not os.path.isdir(os.path.join(output_path, dataset[i])):
            os.makedirs(os.path.join(output_path, dataset[i]))
        dataset_path.append(os.path.join(output_path, dataset[i]))

    for i in range(len(dataset)):
        txtfile = os.path.join(txt_path, dataset[i] + '.txt')

        f = open(txtfile, 'r')
        for line in f.readlines():
            shutil.copy(os.path.join(raw_data_path, line[:-1]), 
                    os.path.join(output_path, dataset[i], line[:-1]))
            # shutil.copy(os.path.join(raw_data_path, line[:-4] + "bmp"), 
            #         os.path.join(output_path, dataset[i], line[:-4] + "bmp"))        
    return dataset_path