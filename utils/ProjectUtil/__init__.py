# -*- coding: utf-8 -*-

"""
Created on FRI MAR 4 17:00:00 2021
@author: ShanYang
"""

import json, jwt, os
from datetime import datetime

key = 'auo'
algorithm = 'HS256'
rootProjectPath = f"./projects"

def decode_key(token):
    try:
        deDict = jwt.decode(token, key, algorithms=[algorithm])
        return True, deDict
    except:
        return False, "Decode key failed"

def create_project(projectName):
    try:
        projectPath = f"{rootProjectPath}/{projectName}"
        if not os.path.isdir(projectPath):
            os.makedirs(f"{projectPath}/experiments")
            os.makedirs(f"{projectPath}/runs")
        projectList = os.listdir(rootProjectPath)
        return True, projectList
    except:
        return False, "Create project failed"

def save_config_as_json(projectName, config):
    try:
        jsonName = datetime.now().strftime('%Y%m%d%H%M%S')
        with open(f"{rootProjectPath}/{projectName}/experiments/{jsonName}.json", 'w') as jsonFile:
            json.dump(config, jsonFile, indent=4)
        return True, f"{rootProjectPath}/{projectName}/experiments/{jsonName}.json"
    except:
        return False, "Save config failed"

def find_project(projectName):
    try:
        projectPath = f"{rootProjectPath}/{projectName}"
        if os.path.isdir(projectPath):
            return True, projectPath
        else:
            return False, "Project doesn't exist"
    except:
        return False, "Find project failed"

def get_config(projectPath):
    try:
        configList = os.listdir(f"{projectPath}/experiments")
        configDict = {}
        for configFile in configList:
            with open(f"{projectPath}/experiments/{configFile}") as jsonFile:
                config = json.load(jsonFile)
                configDict[str(configFile.split('.')[0])] = config
        return True, configDict
    except:
        return False, "Get config failed"

def check_data_uploaded(datasetPath):
    try:
        if not os.path.isdir(f"{datasetPath}"):
            return False, "There is no folder"
        dataList = os.listdir(f"{datasetPath}")
        if not dataList:
            return False, "There is no data"
        return True, dataList
    except:
        return False, "Check data uploaded failed"

def check_data_labeled(datasetPath):
    try:
        classList = []
        dataList = os.listdir(f"{datasetPath}")
        for data in dataList:
            if os.path.isdir(f"{datasetPath}/{data}"):
                if check_class_name_legal(data): 
                    classList.append(data)
        if not classList:
            return False, "There is no classification"
        return True, classList
    except:
        return False, "Check data labeled failed"

def check_class_name_legal(className):
    try:
        illegalName = ["train", "training", "val", "valid", "validation",
                    "test", "testing", "inference", "inf"]
        if illegalName.index(className.lower()):
            return False
    except:
        return True

def check_data_split(datasetPath):
    try:
        datasetList = []
        dataList = os.listdir(f"{datasetPath}")
        for data in dataList:
            if os.path.isdir(f"{datasetPath}/{data}"):
                if not check_class_name_legal(data): 
                    datasetList.append(data)
        if not datasetList:
            return False, "There is no data split"
        return True, datasetList
    except:
        return False, "Check data labeled failed"