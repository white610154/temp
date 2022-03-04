import json, jwt, os
from datetime import datetime

key = 'auo'
algorithm = 'HS256'

def decode_key(token):
    try:
        deDict = jwt.decode(token, key, algorithms=[algorithm])
        return deDict
    except:
        return None

def make_project_folder(projectName):
    try:
        if not os.path.exists(f"./projects/{projectName}"):
            os.makedirs(f"./projects/{projectName}/experiments")
            os.makedirs(f"./projects/{projectName}/runs")
        projectsList = os.listdir(f"./projects/")
        return projectsList
    except:
        return None

def save_config_as_json(projectName, config):
    try:
        jsonName = datetime.now().strftime('%Y%m%d%H%M%S')
        with open(f"./projects/{projectName}/experiments/{jsonName}.json", 'w') as jsonFile:
            json.dump(config, jsonFile)
        return f"./projects/{projectName}/{jsonName}.json"
    except:
        return None

