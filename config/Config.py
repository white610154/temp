# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""

'''
Step1: 設定TASK - 可選擇 "Train"、"Test"、"Inference"
Step2: 設定參數 - 依照所選的TASK，設定所需的參數
'''
class BasicSetting:
    projectID    = 0        # 專案ID
    experimentID = 0        # 實驗ID
    task         = 'Inference'  # 'Train'、'Test' 或 'Inference'


class PrivateSetting:
    datasetPath = "./dataset"
    outputPath  = 'output'
