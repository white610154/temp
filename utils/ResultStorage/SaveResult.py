# -*- coding: utf-8 -*-

"""
Created on Jun Tue 14 22:00:00 2022
"""

import os
from .csvModule import UsingCsv
 ### 阿阿阿世亞這邊不知道怎麼寫回傳, 交給你了

class ResultCsv():
    def __init__(self, result:dict, count:int, mode:str, outputPath:str, classNameList:list, unknownMode:int=None):
        """
        Save result
            1. Wrong result into csv file
            2. Filter out images with scores below the threshold 
            3. Output test result into csv file, file name : Test_result.csv or Inference_result.csv.

        Args:
            result: result from model 
            count: use to record current file
            mode: task - test/ inference
            outputPath: outputPath
            classNameList: class name List
            unknownMode: unknown mode - 1 for only unknown; 2 for all file
        """
        self.filename = result["filename"]
        self.predict = result["predict"]
        self.label = result["label"]
        self.confidence = result["confidence"]
        self.output = result["output"]
        self.mode = mode
        self.count = count
        self.outputPath = outputPath
        self.classNameList = classNameList
        self.unknownMode = unknownMode
        self.create_folder()

    def create_folder(self):
        if not os.path.isdir(self.outputPath):
            os.makedirs(self.outputPath)

    def result_csv(self):
        """
        create result csv file
        Returns:
            UsingCsv class for result csv
        """
        if self.mode == "Test":
            fileName = 'Test_result.csv'
            title = ['Filename', 'Ground truth', 'Prediction']
        elif self.mode == "Inference":
            fileName = 'Inference_result.csv'
            title = ['Filename', 'Prediction']
        title.extend(self.classNameList)
        resultCsv = UsingCsv(fileName, self.outputPath, title)
        if self.count == 0:
            resultCsv.create_csv()
        return resultCsv

    def wrong_csv(self):
        """
        create wrong prediction csv file
        Returns:
            UsingCsv class for wrong prediction csv
        """
        fileName = 'Test_wrong_file.csv'
        title = ['Wrong Filename', 'Ground truth', 'Prediction']
        title.extend(self.classNameList)
        wrongCsv = UsingCsv(fileName, self.outputPath, title)
        if self.count == 0:
            wrongCsv.create_csv()
        return wrongCsv

    def unknown_csv(self):
        """
        create unkwon csv file
        Returns:
            UsingCsv class for unknown csv
        """
        if self.mode == "Test":
            fileName = f'Test_filter.csv' 
            title = ['Filename', 'Ground truth', 'Prediction', 'Sorce']
        elif self.mode == "Inference":
            fileName = f'Inference_filter.csv'
            title = ['Filename', 'Prediction', 'Sorce']
        unknownCsv = UsingCsv(fileName, self.outputPath, title)
        if self.count == 0:
            unknownCsv.create_csv() 
        return unknownCsv

    def write_result(self):
        """
        generate result csv
        """
        resultCsv =  self.result_csv()
        if self.mode == "Test":
            result =  [self.filename, self.label, self.predict]
        else:
            result =  [self.filename, self.predict]
        for className in self.classNameList:
            result.append(f'{self.output[className]:.4f}')
        resultCsv.writing(result, 'a')   

    def write_wrong(self):
        """
        generate wrong prediction csv
        """
        wrongCsv =  self.wrong_csv()
        if self.label != self.predict:
            result =  [self.filename, self.label, self.predict]
            for className in self.classNameList:
                result.append(f'{self.output[className]:.4f}')
            wrongCsv.writing(result, 'a')   
    
    def write_unknown(self):
        """
        generate unknown filtered out csv
        self.unknownMode = 1 for saving result which is unknown
        self.unknownMode = 2 for saving all result, 這個不是跟儲存所有結果一樣嗎XD
        """
        unknownCsv =  self.unknown_csv()
        if self.mode == "Test":
            result =  [self.filename, self.label, self.predict, f'{self.confidence:.4f}']
        else:
            result =  [self.filename, self.predict, f'{self.confidence:.4f}']
        if self.unknownMode == 1 and not self.predict in self.classNameList:
            unknownCsv.writing(result, 'a')   
        elif self.unknownMode == 2:
            unknownCsv.writing(result, 'a')   