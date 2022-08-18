"""
Created on TUE MAR 22 17:00:00 2021
@author: ShanYang
"""

import json, os, shutil, time
import subprocess

# statue
# waiting/ training/ testing

rootProjectPath = f"projects"
runQueueJsonPath = f"main/run_queue.json"

def get_first_run():
    try:
        if not os.path.exists(runQueueJsonPath):
            return False, "there is no run queue"
        with open(runQueueJsonPath, 'r') as queueFile:
            queueDict = json.load(queueFile)
        workList = queueDict["work"]
        if len(workList) <= 0:
            return False, "There is no run"
        return True, workList[0]
    except Exception as err:
        print(err)
        return False, err

def load_run_config(projectName, runId):
    try:
        projectPath = f"{rootProjectPath}/{projectName}"
        configPath = f"{projectPath}/runs/{runId}/{runId}.json"        
        config = None
        if not os.path.exists(configPath):
            return False, "There is no config"
        with open(configPath, 'r') as configFile:
            config = json.load(configFile)
        if not config:
            return False, "There is no config"
        config["Config"]["PrivateSetting"]["datasetPath"] = f'datasets/{config["Config"]["PrivateSetting"]["datasetPath"]}'
        return True, config
    except Exception as err:
        print(err)
        return False, err

def create_config_folder():
    try:
        configFolderPath = f"config"
        if os.path.isdir(configFolderPath):
            shutil.rmtree(configFolderPath)
        os.makedirs(configFolderPath)
        return True
    except Exception as err:
        print(err)
        return False

def modify_config_special_case(config, normalizeName=None):
    if normalizeName != None:
        try:
            _ = config["ConfigPreprocess"]["PreprocessPara"]["normalize"]
            if config["ConfigPreprocess"]["PreprocessPara"]["normalize"]["mode"] in ["CalculateFromData", "UserInput"]:
                config["ConfigPreprocess"]["PreprocessPara"]["normalize"]["mode"] = normalizeName
        except:
            pass

def create_python_config(config, projectName, experimentId, runId, task):
    try:
        modify_config_special_case(config, normalizeName=f'{projectName}-{runId}')
        configFileList = ["Config", "ConfigAugmentation", "ConfigEvaluation", "ConfigModelService",
                          "ConfigPostprocess", "ConfigPreprocess", "ConfigPytorchModel", "ConfigResultStorage"]
        for configFileName in configFileList:
            if configFileName in config:
                ok = write_python_config(configFileName, config[configFileName], mode=1)
                if not ok:
                    return False
            else:
                ok = write_python_config(configFileName, None, mode=0)
                if not ok:
                    return False
        projectConfigList = {
            "BasicSetting": {
                "projectName": projectName,
                "runId": runId,
                "task": task
                }
            }
        ok = write_python_config("Config", projectConfigList, mode=2)
        if not ok:
            return False
        ok = transform_model()
        if not ok:
            return False
        return True

    except Exception as err:
        print(err)
        return False

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
                for configParameter in configList[config]:
                    if parameter == configParameter:
                        replaceWord = configList[config][configParameter]
                        if isinstance(configList[config][configParameter], str):
                            replaceWord = f"'{configList[config][configParameter]}'"
                        lines[parameterDict[parameter][0]] = f'{lines[parameterDict[parameter][0]][0:parameterDict[parameter][1]]} {replaceWord}\n'

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
        with open(f"sample/model_transform.json") as jsonFile:
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

def move_first_run():
    try:
        if not os.path.exists(runQueueJsonPath):
            return False, "there is no run queue"
        with open(runQueueJsonPath, 'r') as queueFile:
            queueDict = json.load(queueFile)
        doneList = queueDict["done"]
        workList = queueDict["work"]
        doneList.append(workList[0])
        del(workList[0])
        queueDict = {"done": doneList, "work": workList}
        with open(runQueueJsonPath, 'w') as queueFile:
            json.dump(queueDict, queueFile, indent = 4)
        return True
    except Exception as err:
        print(err)
        return False

def delete_config():
    try:
        if not os.path.exists(f"config"):
            return False, "there is no config folder"
        shutil.rmtree(f"config")
        return True
    except Exception as err:
        print(err)
        return False

def run_model():
    try:
        modelMainPath = './sample/ModelMain.py'
        runModelMainPath = './ModelMain.py'
        shutil.copyfile(modelMainPath, runModelMainPath)
        if os.path.isfile("ModelMain.exe"):
            proc = subprocess.Popen(["ModelMain.exe"], stdout=subprocess.PIPE, shell=True)
        else:
            proc = subprocess.Popen(["python", "ModelMain.py"], stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        print(out)
        if err != None:
            print(err)
        os.remove(runModelMainPath)
        return True, None
    except Exception as err:
        print("run train failed:", err)
        return False, err

def run_process():
    while True:
        time.sleep(1)
        try:      
            ok, run = get_first_run()
            if ok:
                print('=' * len(str(run)))
                print(run)
            if not ok:
                # print(run)
                continue
            ok, config = load_run_config(run["projectName"], run["runId"])
            if not ok:
                continue
            ok = create_config_folder()
            if not ok:
                continue
            ok = create_python_config(config, **run)
            if not ok:
                continue
            ok, err = run_model()
            if not ok:
                # 存結果 err
                continue
            ok = move_first_run()
            if not ok:
                continue
            ok = delete_config()
            if not ok:
                continue
        except Exception as err:
            # _ = delete_first_run()
            _ = delete_config()
            print(err)

if __name__ == "__main__":
    run_process()