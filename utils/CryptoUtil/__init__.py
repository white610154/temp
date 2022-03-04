# -*- coding: utf-8 -*-

"""
Created on FRI MAR 4 17:00:00 2021
@author: ShanYang
"""

import json, jwt, os
from datetime import datetime

key = 'auo'
algorithm = 'HS256'
projectsPath = f"./projects"

def decode_key(token):
    try:
        deDict = jwt.decode(token, key, algorithms=[algorithm])
        return deDict
    except:
        return None

def create_project(projectName):
    try:
        projectPath = f"{projectsPath}/{projectName}"
        if not os.path.exists(projectPath):
            os.makedirs(f"{projectPath}/experiments")
            os.makedirs(f"{projectPath}/runs")
        projectsList = os.listdir(projectsPath)
        return projectsList
    except:
        return None

def find_project(projectName):
    try:
        projectPath = f"{projectsPath}/{projectName}"
        if os.path.exists(projectPath):
            return projectPath
        else:
            return False
    except:
        return none

def save_config_as_json(projectName, config):
    try:
        jsonName = datetime.now().strftime('%Y%m%d%H%M%S')
        with open(f"./projects/{projectName}/experiments/{jsonName}.json", 'w') as jsonFile:
            json.dump(config, jsonFile, indent=4)
        return f"./projects/{projectName}/{jsonName}.json"
    except:
        return None

def get_config(projectFolderPath):
    try:
        configsList = os.listdir(f"{projectFolderPath}/experiments")
        configDict = {}
        for configFile in configsList:
            with open(f"{projectFolderPath}/experiments/{configFile}") as jsonFile:
                config = json.load(jsonFile)
                configDict[str(configFile.split('.')[0])] = config
        return configDict
    except:
        return None

    
    



