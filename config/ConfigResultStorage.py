# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""

##### 模型參數設定 #####
class ResultStorage:
    saveFinalWeight = False
    saveCheckpoint  = {'switch': False, 'saveIter': 1}
    saveAccTxt      = True
    drawAccCurve    = True
    drawConfusionMatrix = True
