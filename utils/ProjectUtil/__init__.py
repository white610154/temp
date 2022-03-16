# -*- coding: utf-8 -*-

"""
Created on FRI MAR 4 17:00:00 2021
@author: ShanYang
"""

import json, jwt, os, shutil
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
        if os.path.isdir(projectPath):
            return False, "Project already exists"
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

        config['Config']['PrivateSetting']['datasetPath'] = datasetPath
        with open(configPath, 'w') as fout:
            json.dump(config, fout, indent=4)
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
                if data == "Train":
                    isTrain = 1
                    datasetList.append(data)
                elif data == "Valid":
                    isValid = 1
                    datasetList.append(data)
                elif data == "Test":
                    isTest = 1
                    datasetList.append(data)
        if isTrain == 1 and isValid == 1 and isTest == 1:
            return True, datasetList
        return False, "Please set Train/ Valid/ Test"
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
                json.dump(datasets, fout, indent=4)
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
            json.dump(datasets, fout, indent=4)
    except Exception as err:
        print(err)

def create_python_config(projectName, experimentId, task):
    try:
        projectPath = f"{rootProjectPath}/{projectName}"
        runId = create_run(projectPath, experimentId)
        if not runId:
            return False, "create run failed"
        
        ConfigPath = f"{projectPath}/runs/{runId}/{runId}.json"        
        config = None
        with open(ConfigPath, 'r') as configFile:
            config = json.load(configFile)
        if not config:
            return False, "Load config failed"

        configFolderPath = f"config"
        if os.path.isdir(configFolderPath):
            shutil.rmtree(configFolderPath)
        os.makedirs(configFolderPath)

        configFileList = ["Config", "ConfigAugmentation", "ConfigEvaluation", "ConfigModelService",
                          "ConfigPostprocess", "ConfigPreprocess", "ConfigPytorchModel", "ConfigResultStorage"]
        for configFileName in configFileList:
            if configFileName in config:
                ok = write_python_config(configFileName, config[configFileName], mode=1)
                if not ok:
                    return False, "write model service failed"
            else:
                ok = write_python_config(configFileName, None, mode=0)
                if not ok:
                    return False, "write model service failed"
        
        projectConfigList = {
            "BasicSetting": {
                "projectName": projectName,
                "runId": runId,
                "task": task
                }
            }
        ok = write_python_config("Config", projectConfigList, mode=2)
        if not ok:
            return False, "set project information failed"
        
        ok = transform_model()
        if not ok:
            return False, "transform model failed"
        return True, config

    except Exception as err:
        print(err)
        return False, err

def create_run(projectPath, experimentId):
    try:
        runName = datetime.now().strftime('%Y%m%d%H%M%S')
        runPath = f"{projectPath}/runs/{runName}"
        if os.path.isdir(runPath):
            return False, "Run already exists"
        os.makedirs(runPath)
        experimentConfigPath = f"{projectPath}/experiments/{experimentId}.json"
        runConfigPath = f"{runPath}/{runName}.json"
        shutil.copy(experimentConfigPath, runConfigPath)
        return runName
    except:
        return None

def write_python_config(configFileName, configList, mode):
    '''
    mode = 0: copy
    mode = 1: write a new config
    mode = 2: rewrite a config
    '''
    try:
        if mode == 0:
            sampleConfigPath = f"sample/Config/{configFileName}.py"
            configPath = f"config/{configFileName}.py"
            shutil.copy(sampleConfigPath, configPath)
            return True
        
        sampleConfigPath = f"sample/Config/{configFileName}.py"
        if mode == 2:
            sampleConfigPath = f"config/{configFileName}.py"
        configPath = f"config/{configFileName}.py"
        lines = []
        with open(sampleConfigPath, "r") as sampleConfigFile:
            fileLines = sampleConfigFile.readlines()
            for fileLine in fileLines:
                lines.append(fileLine)
                
        classLineNumDict = get_class_line_num(lines, configList)
        if not classLineNumDict:
            return False

        for config in configList:
            parameterDict = get_parameter(lines, classLineNumDict[config][0], classLineNumDict[config][1])
            if not parameterDict:
                return False

            for parameter in parameterDict:
                for config_parameter in configList[config]:
                    if parameter == config_parameter:
                        replace_word = configList[config][config_parameter]
                        if isinstance(configList[config][config_parameter], str):
                            replace_word = f'"{configList[config][config_parameter]}"'
                        lines[parameterDict[parameter][0]] = f"{lines[parameterDict[parameter][0]][0:parameterDict[parameter][1]]} {replace_word}\n"

        with open(configPath, "w") as ConfigFile:
            for line in lines:
                ConfigFile.write(line)
        return True
    except:
        return False

def get_class_line_num(lines, configList):
    try:
        classLineNumDict = {}
        for config in configList:
            line_cnt = 0
            isClass = False
            for line_cnt in range(0, len(lines)):
                if isClass == False:
                    if lines[line_cnt].find(config) >= 0:
                        classLineNumDict[config] = [line_cnt, -1]
                        isClass = True
                elif isClass == True:
                    if lines[line_cnt].find("class") >= 0:
                        classLineNumDict[config] = [classLineNumDict[config][0], line_cnt]
                        break
            if classLineNumDict[config][-1] == -1:
                classLineNumDict[config] = [classLineNumDict[config][0], len(lines)]
        return classLineNumDict
    except:
        return None

def get_parameter(lines, start_location, end_location):
    try:
        parameterDict = {}
        for line_cnt in range(start_location, end_location + 1):
                if line_cnt < len(lines):
                    equal_location = lines[line_cnt].find("=")
                    if equal_location >= 0:
                        parameter = lines[line_cnt][0:equal_location].replace(" ", "")
                        parameterDict[parameter] = [line_cnt, equal_location + 1]
        return parameterDict
    except:
        return None

def transform_model():
    try:
        modelTransDict = None
        with open(f"./sample/model_transform.json") as jsonFile:
            modelTransDict = json.load(jsonFile)
        if not modelTransDict:
            return False
        lines = []
        configPath = f"config/ConfigPytorchModel.py"
        with open(configPath, "r") as configFile:
            fileLines = configFile.readlines()
            for fileLine in fileLines:
                lines.append(fileLine)
        newLines = []
        for line in lines:
            for origianlModel in modelTransDict:
                if line.find(origianlModel) >= 0:
                    line = line.replace(origianlModel, modelTransDict[origianlModel])
                    break
            newLines.append(line)
        with open(configPath, "w") as configFile:
            for newLine in newLines:
                configFile.write(newLine)
        return True
    except:
        return False