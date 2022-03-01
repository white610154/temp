# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""
from config.Config import PrivateSetting
from config.ConfigPytorchModel import ClsModelPara

##### 模型參數設定 #####
class LossFunctionPara:
    ### CrossEntropyLoss, MSELoss, L1Loss, SmoothL1Loss, BCELoss
    lossFunction = 'CrossEntropyLoss'


class LearningRate:
    learningRate = 0.01


class OptimizerPara:
    ### SGD, Adam, Adadelta, AdamW, (NAdam: torch=1.10)
    SGD      = {'switch': False, 'momentum': 0.9, 'dampening': 0, 'weightDecay': 5e-4, 'nesterov': False}
    Adam     = {'switch': True, 'betas': (0.9, 0.999), 'eps': 1e-8, 'weightDecay': 5e-4, 'amsgrad': False}
    Adadelta = {'switch': False, 'rho': 0.9, 'eps': 1e-6, 'weightDecay': 0}
    AdamW    = {'switch': False, 'betas': (0.9, 0.999), 'eps': 1e-8, 'weightDecay': 0.01, 'amsgrad': False}
    NAdam    = {'switch': False, 'betas': (0.9, 0.999), 'eps': 1e-08, 'weightDecay': 0, 'momentumDecay': 0.004}
    # NAdam needs torch version= 1.10.0 up

class SchedulerPara:
    # 使用pytorch官方method，參數名稱是否修改為mmfaa1 coding rule ?
    stepLR = {'switch': True, 'step_size': 1, 'gamma': 0.5}
    cosineAnnealingLR = {'switch': False, 'T_max': ClsModelPara.epochs, 'eta_min': 0}



   
