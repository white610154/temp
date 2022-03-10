# -*- coding: utf-8 -*-

"""
Created on FRI MAR 4 17:00:00 2021
@author: ShanYang
"""

import json, jwt, os
from pkgutil import get_data
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

def get_projects():
    try:
        return True, os.listdir(rootProjectPath)
    except:
        return False, "Get projects failed"

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

def set_config_dataset(projectPath, experimentId, datasetPath):
    try:
        configPath = f"{projectPath}/experiments/{experimentId}.json"
        if not os.path.isfile(configPath):
            return False, "Experiment not found"

        datasets = get_datasets(projectPath)
        if not datasets or not datasetPath in datasets:
            return False, "Dataset not found"

        config = None
        with open(configPath, 'r') as fin:
            config = json.load(fin)
        if not config:
            return False, "Load config failed"

        config['Config']['datasetPath'] = datasetPath
        with open(configPath, 'w') as fout:
            json.dump(config, fout)
        return True, config
    except Exception as err:
        print(err)
        return False, err

def check_data_uploaded(datasetPath):
    try:
        if not os.path.isdir(datasetPath):
            return False, "There is no folder"
        dataList = os.listdir(datasetPath)
        if not dataList:
            return False, "There is no data"
        return True, dataList
    except:
        return False, "Check data uploaded failed"

def check_data_split(datasetPath):
    try:
        isTrain = isValid = isTest = 0
        datasetList = []
        dataList = os.listdir(datasetPath)
        for data in dataList:
            if os.path.isdir(f"{datasetPath}/{data}"):
                if data == "train":
                    isTrain = 1
                    datasetList.append(data)
                elif data == "valid":
                    isValid = 1
                    datasetList.append(data)
                elif data == "test":
                    isTest = 1
                    datasetList.append(data)
        if isTrain == 1 and isValid == 1 and isTest == 1:
            return True, datasetList
        return False, "Please set train/ valid/ test"
    except:
        return False, "Check data split failed"

def check_data_labeled(datasetPath):
    try:
        classList = []
        dataList = os.listdir(datasetPath)
        for data in dataList:
            if os.path.isdir(f"{datasetPath}/{data}"):
                if check_class_name_legal(data): 
                    classList.append(data)
        if not classList:
            return False, "There is no classify"
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

def get_datasets(projectPath):
    try:
        datasets = {}
        datasetFilePath = f"{projectPath}/datasets.json"
        if os.path.exists(datasetFilePath):
            with open(f"{projectPath}/datasets.json", 'r') as fin:
                datasets = json.load(fin)
        return datasets
    except Exception as err:
        print(err)

def remove_dataset(projectPath, datasetPath):
    try:
        datasets = {}
        datasetFilePath = f"{projectPath}/datasets.json"
        if os.path.exists(datasetFilePath):
            with open(f"{projectPath}/datasets.json", 'r') as fin:
                datasets = json.load(fin)
        if datasetPath in datasets:
            del datasets[datasetPath]
            with open(f"{projectPath}/datasets.json", 'w') as fout:
                json.dump(datasets, fout)
        return datasets
    except Exception as err:
        print(err)

def add_dataset(projectPath, datasetPath, uploaded=False, labeled=False, split=False):
    try:
        datasets = {}
        datasetFilePath = f"{projectPath}/datasets.json"
        if os.path.exists(datasetFilePath):
            with open(f"{projectPath}/datasets.json", 'r') as fin:
                datasets = json.load(fin)
        
        datasets[datasetPath] = {
            'uploaded': uploaded,
            'labeled': labeled,
            'split': split,
        }

        with open(f"{projectPath}/datasets.json", 'w') as fout:
            json.dump(datasets, fout)
    except Exception as err:
        print(err)