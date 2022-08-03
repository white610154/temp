import hashlib
import json
import os
import shutil
from datetime import datetime, timedelta

def get_deploy_path_information(projectName, deployPath: str):
    fullDeployPath = f'deploy/{deployPath}'
    if not os.path.isdir(fullDeployPath):
        return False, "folder not exists"

    infoPath = f'{fullDeployPath}/.auosala'
    info = {}
    if os.path.isfile(infoPath):
        with open(infoPath, 'r') as f:
            info = json.load(f)

    if not projectName in info:
        info[projectName] = []

    with open(infoPath, 'w') as f:
        json.dump(info, f)

    return True, info

def set_deploy_path_information(projectName, deployPath, deployInfo):
    fullDeployPath = f'deploy/{deployPath}'
    if not os.path.isdir(fullDeployPath):
        return False, "folder not exists"

    try:
        infoPath = f'{fullDeployPath}/.auosala'
        info = {}
        with open(infoPath, 'r') as f:
            info = json.load(f)

        info[projectName].append({
            'date': (datetime.today() + timedelta(hours=8)).strftime("%Y/%m/%d"),
            **deployInfo,
        })
        with open(infoPath, 'w') as f:
            json.dump(info, f)

        return True, info
    except Exception as err:
        return False, f"Set deploy information failed: {err}"


def get_deploy_path(projectPath):
    try:
        deploySettingPath = f'{projectPath}/deploy.json'
        if os.path.isfile(deploySettingPath):
            with open(deploySettingPath, 'r') as fin:
                deployPathList = json.load(fin)
        else:
            return False, "Deploy path not set"
        return True, deployPathList[0]
    except:
        return False, "Get deploy path failed"


def set_deploy_path(projectPath, deployPath):
    try:
        deploySettingPath = f'{projectPath}/deploy.json'
        deployPathList = []
        if os.path.isfile(deploySettingPath):
            with open(deploySettingPath, 'r') as fin:
                deployPathList = json.load(fin)
        deployPathList = [deployPath]
        with open(deploySettingPath, 'w') as fout:
            json.dump(deployPathList, fout)
        return True
    except:
        return False


def deploy(projectName, projectPath, runId, filename):
    try:
        ok, deployPath = get_deploy_path(projectPath)
        if not ok:
            return False, deployPath

        ok, onnxPath, onnxFile, iniFile = find_onnx(projectPath, runId)
        if not ok:
            return False, onnxPath

        src = os.path.join(onnxPath, onnxFile)
        dst = os.path.join('deploy', deployPath, f'{filename}.onnx')
        shutil.copy(src, dst)

        isrc = os.path.join(onnxPath, iniFile)
        idst = os.path.join('deploy', deployPath, f'{filename}.ini')
        shutil.copy(isrc, idst)

        ok, message = set_deploy_path_information(projectName, deployPath, {
            'runId': runId,
            'fileChecksum': get_md5(src),
            'filename': filename,
        })
        if not ok:
            return False, message

        return True, message

    except Exception as err:
        return False, f"Deploy failed: {err}"


def get_md5(filepath):
    md5_hash = hashlib.md5()

    with open(filepath, "rb") as f:
        content = f.read()
        md5_hash.update(content)

    digest = md5_hash.hexdigest()
    return digest

def find_onnx(projectPath: str, runId: str):
    try:
        onnxPath = os.path.abspath(f'{projectPath}/runs/{runId}')
        onnxFile = f'BestOnnx.onnx'
        iniFile = f'BestOnnx.ini'
        if not os.path.isfile(os.path.join(onnxPath, onnxFile)):
            return False, "Model not found", None
        return True, onnxPath, onnxFile, iniFile
    except Exception as err:
        print(err)
        return False, err, None, None

def checkFile(deployPath, modelName, fileChecksum):
    if os.path.isfile(os.path.join('deploy', deployPath, f'{modelName}.onnx')):
        return get_md5(modelName) == fileChecksum
    return False
