# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""

class BasicSetting:
    projectID    = 0         # Project ID
    experimentID = 0         # Experiment ID
    task         = "Train"   # 'Train', 'Test' or 'Inference'

class PrivateSetting:
    datasetPath = "./dataset" # The path for data clean.
    outputPath  = "output"    # The path that all result place.
