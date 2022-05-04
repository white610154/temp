# -*- coding: utf-8 -*-

"""
Created on FRI MAR 4 17:00:00 2021
@author: ShanYang
"""

import json, jwt, os, shutil
from datetime import datetime

key = 'auo'
algorithm = 'HS256'
rootProjectPath = f'./projects'

### project

def decode_key(token):
    try:
        deDict = jwt.decode(token, key, algorithms=[algorithm])
        return True, deDict
    except:
        return False, 'Decode key failed'

def create_project(projectName):
    try:
        if os.path.isdir(f'{rootProjectPath}/{projectName}'):
            return False, 'Project already exists'
        os.makedirs(f'{rootProjectPath}/{projectName}/experiments')
        os.makedirs(f'{rootProjectPath}/{projectName}/runs')
        return True, 'success'
    except:
        return False, 'Create project failed'

def save_config_as_json(projectName, config):
    try:
        jsonName = datetime.now().strftime('%Y%m%d%H%M%S')
        with open(f'{rootProjectPath}/{projectName}/experiments/{jsonName}.json', 'w') as jsonFile:
            json.dump(config, jsonFile, indent=4)
        return True, f'{rootProjectPath}/{projectName}/experiments/{jsonName}.json'
    except:
        return False, 'Save config failed'

def get_projects():
    try:
        return True, os.listdir(rootProjectPath)
    except:
        return False, f'Get projects failed'

def delete_project(projectPath):
    try:
        shutil.rmtree(projectPath)
        return True, "Success"
    except:
        return False, "Delete project failed"

def find_project(projectName):
    try:
        projectPath = f'{rootProjectPath}/{projectName}'
        if os.path.isdir(projectPath):
            return True, projectPath
        else:
            return False, "Project doesn't exist"
    except:
        return False, "Find project failed"

### experiment

def get_config(projectPath):
    try:
        configList = os.listdir(f'{projectPath}/experiments')
        configDict = {}
        for configFile in configList:
            with open(f'{projectPath}/experiments/{configFile}') as jsonFile:
                config = json.load(jsonFile)
                configDict[str(configFile.split('.')[0])] = config
        return True, configDict
    except:
        return False, "Get config failed"

def set_config_dataset(projectPath, experimentId, datasetPath):
    try:
        configPath = f'{projectPath}/experiments/{experimentId}.json'
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

def save_run_in_queue(runInfo, task):
    '''
    save a run process in run queue
    '''
    try:
        projectName = runInfo["projectName"]
        experimentId = runInfo["experimentId"]
        projectPath = f"{rootProjectPath}/{projectName}"
        if task == 'Train':
            runId = create_run(projectPath, experimentId)
            if not runId:
                return False, "create run failed"
        elif task == 'Test':
            runId = runInfo["runId"]
        runQueueJsonPath = f"main/run_queue.json"
        workList = []
        newRun = {
                "projectName": projectName,
                "experimentId": experimentId,
                "runId": runId,
                "task": task
            }
        if os.path.exists(runQueueJsonPath):
            with open(runQueueJsonPath, 'r') as queueFile:
                queueDict = json.load(queueFile)
            doneList = queueDict["done"]
            workList = queueDict["work"]
        workList.append(newRun)
        queueDict = {"done": doneList, "work": workList}
        with open(runQueueJsonPath, 'w') as queueFile:
            json.dump(queueDict, queueFile, indent = 4)
        return True, newRun

    except Exception as err:
        print(err)
        return False, err

def create_run(projectPath, experimentId):
    """
    1. create run folder
    2. copy exp config to run
    """
    try:
        runName = datetime.now().strftime('%Y%m%d%H%M%S')
        runPath = f"{projectPath}/runs/{runName}"
        if os.path.isdir(runPath):
            return False
        os.makedirs(runPath)
        experimentConfigPath = f"{projectPath}/experiments/{experimentId}.json"
        runConfigPath = f"{runPath}/{runName}.json"
        shutil.copy(experimentConfigPath, runConfigPath)
        return runName
    except Exception as err:
        print(err)
        return None

def get_runs():
    try:
        runQueueJsonPath = f"main/run_queue.json"
        if not os.path.exists(runQueueJsonPath):
            return False, "there is no run queue"
        with open(runQueueJsonPath) as jsonFile:
            jsonDict = json.load(jsonFile)
        #     queue = jsonDict["queue"]
        # if len(queue) <= 0:
        #     return False, "There is no run"
        return True, jsonDict
    except Exception as err:
        print(err)
        return False, err

def get_queue_process(runDict, mode):
    try:
        if mode == "work":
            wrongMsg = "Training has not started"
        else:
            wrongMsg = "This run has been deleted"
        runProcessPath = f'./projects/{runDict["projectName"]}/runs/{runDict["runId"]}/model{runDict["task"]}ing.json'
        if not os.path.exists(runProcessPath):
            runDict["process"] = wrongMsg
            return False, runDict
        with open(runProcessPath) as jsonFile:
            trainingProcess = json.load(jsonFile)
            runDict["process"] = trainingProcess
        return True, runDict
    except Exception as err:
        print(err)
        return False, err

def delete_run_in_queue(projectName, runId):
    try:
        runQueueJsonPath = f"main/run_queue.json"
        if not os.path.exists(runQueueJsonPath):
            return False, "there is no run queue"
        with open(runQueueJsonPath) as jsonFile:
            jsonDict = json.load(jsonFile)
            doneList = jsonDict["done"]
            workList = jsonDict["work"]
        if len(workList) > 0:
            if workList[0]["projectName"] == projectName and workList[0]["runId"] == runId:
                return False, "This run is running"
        newDoneList = []
        for done in doneList:
            if done["projectName"] != projectName or done["runId"] != runId:
                newDoneList.append(done)
        newWorkList = []
        for work in workList:
            if work["projectName"] != projectName or work["runId"] != runId:
                newWorkList.append(work)
        jsonDict = {"done": newDoneList, "work": newWorkList}
        with open(runQueueJsonPath, 'w') as jsonFile:
            json.dump(jsonDict, jsonFile, indent=4)
        return True, jsonDict
    except Exception as err:
        print(err)
        return False, err

def find_onnx(projectPath: str, runId: str):
    try:
        onnxPath = os.path.abspath(f'{projectPath}/runs/{runId}/{runId}.onnx')
        if not os.path.isfile(onnxPath):
            return False, "Model not found"
        return True, onnxPath
    except Exception as err:
        print(err)
        return False, err
