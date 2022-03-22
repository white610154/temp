# -*- coding: utf-8 -*-

"""
Created on TUE Dec 7 20:00:00 2021
@author: OtisChang
"""
from config.Config import BasicSetting
from utils.ModelService.PytorchClassificationModel import MainProcess

def train():
    MainProcess.train()

def test():
    MainProcess.test()
    
def inference():
    MainProcess.inference()


def ai_model():
    print(f"========== Project: {BasicSetting.projectName}, Run:{BasicSetting.runId}, Mode:{BasicSetting.task} ==========")
    
    if BasicSetting.task == 'Train':
        train()
    elif BasicSetting.task == 'Test':
        test()
    elif BasicSetting.task == 'Inference':
        inference()
    else:
        raise BaseException("Please set up the correct task mode in config/Config.py.")
