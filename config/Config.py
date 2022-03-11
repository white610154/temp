# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""

class BasicSetting:
    projectID    = ""
    experimentID = ""
    task         = "Train"

class PrivateSetting:
    datasetPath = ""
    outputPath  = f"./projects/{projectID}/runs/{experimentID}"
