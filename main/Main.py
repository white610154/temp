import os
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from utils import ProjectUtil
from utils.ProjectUtil import DeployUtil, ExperimentConfig, FolderUtil, ModelDescription

def response(code, message, data=None):
    # code=0 for success, code=1 for fail
    return {'code': code, 'message': message, 'data': data}

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
CORS(app)

### project

@app.route('/create-project-by-key', methods=['POST'])
def create_project_by_key():
    '''
    input: name, config/ output: prejectList
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'name' in data or not 'key' in data:
        return response(1, "There is no name or key.")

    ok, config = ProjectUtil.decode_key(data['key'])
    if not ok:
        return response(1, config)

    ok, message = ProjectUtil.create_project(data['name'])
    if not ok:
        return response(1, message)

    ok, configPath = ProjectUtil.save_config_as_json(data['name'], config)
    if not ok:
        return response(1, configPath)

    ok, projectList = ProjectUtil.get_projects()
    if not ok:
        return response(1, projectList)
    
    return response(0, "success", {"projects": projectList})

@app.route('/remove-project', methods=['POST'])
def remove_projects():
    '''
    input: projectName/ output: projectList
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data:
        return response(1, "There is no projectName.")
    
    ok, projectPath = ProjectUtil.find_project(data["projectName"])
    if not ok:
        return response(1, projectPath)
    
    ok, message = ProjectUtil.delete_project(projectPath)
    if not ok:
        return response(1, message)
    
    ok, projectList = ProjectUtil.get_projects()
    if not ok:
        return response(1, projectList)
    
    return response(0, "success", {'projects': projectList})

@app.route('/get-projects', methods=['POST', 'GET'])
def get_projects():
    '''
    input: / output: projectList
    '''
    ok, projectList = ProjectUtil.get_projects()
    if not ok:
        return response(1, projectList)

    return response(0, "success", {'projects': projectList})

@app.route('/check-project', methods=['POST'])
def check_project():
    '''
    input: projectName/ output: projectPath
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data:
        return response(1, "There is no projectName.")
    
    ok, projectPath = ProjectUtil.find_project(data["projectName"])
    if not ok:
        return response(1, projectPath)

    return response(0, "success", {'projectPath': projectPath})

### experiment

@app.route('/get-experiments', methods=['POST'])
def get_experiments():
    '''
    input: projectName/ output: config
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data:
        return response(1, "There is no projectName.")
    
    ok, projectPath = ProjectUtil.find_project(data['projectName'])
    if not ok:
        return response(1, projectPath)

    ok, config = ProjectUtil.get_config(projectPath)
    if not ok:
        return response(1, config)

    return response(0, "success", config)

@app.route('/set-experiments', methods=['POST'])
def set_experiments():
    '''
    input: projectName, experiment/ output: experiment
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'experimentId' in data or not 'experiment' in data:
        return response(1, "There is no projectName.")
    
    ok, projectPath = ProjectUtil.find_project(data['projectName'])
    if not ok:
        return response(1, projectPath)

    ok, config = ProjectUtil.set_config(projectPath, data['experimentId'], data['experiment'])
    if not ok:
        return response(1, config)

    return response(0, "success", config)

@app.route('/check-experiment', methods=['POST'])
def check_experiments():
    '''
    input: projectName, experimentId/ output: experimentJsonPath
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'experimentId' in data:
        return response(1, "There is no projectName or experimentId.")
    
    ok, projectPath = ProjectUtil.find_project(data["projectName"])
    if not ok:
        return response(1, projectPath)

    ok, experimentJsonPath = ProjectUtil.find_experiment(projectPath, data['experimentId'])
    if not ok:
        return response(1, experimentJsonPath)

    return response(0, "success", experimentJsonPath)

### dataset

@app.route('/check-dataset', methods=['POST'])
def check_dataset():
    '''
    input: projectName, datasetPath/ output: {uploaded: bool, labeled: bool, split: bool}
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'datasetPath' in data:
        return response(1, "There is no projectName or datasetPath.")

    status = {
        'uploaded': False,
        'labeled': False,
        'split': False
    }

    path = os.path.join('datasets', data['datasetPath'])

    ok, message = ProjectUtil.check_data_uploaded(path)
    if not ok:
        return response(1, message)
    status['uploaded'] = True

    ok, message = ProjectUtil.check_data_split(path)
    if ok:
        status['split'] = True
        datasetPath = f'{path}/Train'
    elif not ok:
        datasetPath = path
    
    ok, message = ProjectUtil.check_data_labeled(datasetPath)
    if not ok:
        return response(1, message)
    
    status['labeled'] = True

    ok, projectPath = ProjectUtil.find_project(data['projectName'])
    if not ok:
        return response(1, projectPath)
    
    ok, message = ProjectUtil.add_dataset(projectPath, data["datasetPath"], **status)
    if not ok:
        return response(1, message)

    return response(0, "success", status)

@app.route('/remove-dataset', methods=['POST'])
def remove_dataset():
    '''
    input: projectName, datasetPath/ output: datasets
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'datasetPath' in data:
        return response(1, "There is no projectName or datasetPath.")

    ok, projectPath = ProjectUtil.find_project(data['projectName'])
    if not ok:
        return response(1, projectPath)

    ok, datasets = ProjectUtil.remove_dataset(projectPath, data['datasetPath'])
    if not ok:
        return response(1, datasets)
    
    return response(0, "success", datasets)

@app.route('/get-datasets', methods=['POST'])
def get_datasets():
    '''
    input: projectName/ output: datasets
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data:
        return response(1, "There is no data.")

    ok, projectPath = ProjectUtil.find_project(data['projectName'])
    if not ok:
        return response(1, projectPath)

    ok, datasets = ProjectUtil.get_datasets(projectPath)
    if not ok:
        return response(1, datasets)
    
    return response(0, "success", datasets)

@app.route('/set-experiment-dataset', methods=['POST'])
def set_experiment_dataset():
    '''
    input: projectName, experimentId, dataPath/ output: config
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'experimentId' in data or not 'datasetPath' in data:
        return response(1, "There is no projectName or experimentId or datasetPath.")
    
    ok, projectPath = ProjectUtil.find_project(data['projectName'])
    if not ok:
        return response(1, projectPath)

    ok, config = ProjectUtil.set_config_dataset(projectPath, data['experimentId'], data['datasetPath'])
    if not ok:
        return response(1, config)
    
    return response(0, "success", config)

### run

@app.route('/run-experiment-train', methods=['POST'])
def run_experiment_train():
    '''
    input: projectName, experimentId/ output: projectName, experimentId, runId, task
    '''
    data = request.get_json()
    if not data:
        return response(1, 'There is no data.')
    elif not 'projectName' in data or not 'experimentId' in data:
        return response(1, 'There is no projectName or experimentId.')
    
    ok, projectPath = ProjectUtil.find_project(data["projectName"])
    if not ok:
        return response(1, projectPath)

    ok, experimentJsonPath = ProjectUtil.find_experiment(projectPath, data['experimentId'])
    if not ok:
        return response(1, experimentJsonPath)

    ok, msg = ProjectUtil.save_run_in_queue(data, task="Train")
    if not ok:
        return response(1, msg)
    return response(0, "success", msg)

@app.route('/run-experiment-test', methods=['POST'])
def run_experiment_test():
    '''
    input: projectName, experimentId/ output: projectName, experimentId, runId, task
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'experimentId' in data or not 'runId' in data:
        return response(1, "There is no data.")
    
    ok, projectPath = ProjectUtil.find_project(data["projectName"])
    if not ok:
        return response(1, projectPath)

    ok, experimentJsonPath = ProjectUtil.find_experiment(projectPath, data['experimentId'])
    if not ok:
        return response(1, experimentJsonPath)

    ok, runJsonPath = ProjectUtil.find_run(projectPath, data['runId'])
    if not ok:
        return response(1, runJsonPath)

    ok, msg = ProjectUtil.save_run_in_queue(data, task="Test")
    if not ok:
        return response(1, msg)
    return response(0, "success", msg)

@app.route('/remove-run-in-queue', methods=['POST'])
def remove_run_in_queue():
    '''
    input: projectName, runId/ output: none
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'runId' in data:
        return response(1, "There is no data.")
    ok, msg = ProjectUtil.delete_run_in_queue(data["projectName"], data["runId"])
    if not ok:
        return response(1, msg)

    return response(0, "success")

@app.route('/remove-run', methods=['POST'])
def remove_run():
    '''
    input: projectName, runId/ output: none
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'runId' in data:
        return response(1, "There is no data.")
    
    ok, projectPath = ProjectUtil.find_project(data["projectName"])
    if not ok:
        return response(1, projectPath)

    ok, runJsonPath = ProjectUtil.find_run(projectPath, data['runId'])
    if not ok:
        return response(1, runJsonPath)
    
    ok, msg = ProjectUtil.delete_run(projectPath, data["runId"])
    if not ok:
        return response(1, msg)

    return response(0, "success")

@app.route('/get-queue-information', methods=['POST'])
def get_queue_information():
    '''
    get queue information
    '''
    ok, queue = ProjectUtil.get_runs()
    if not ok:
        return response(1, queue)
    newQueue = {"done": queue["done"], "work": queue["work"]}
    if len(queue["done"]) > 0:
        newDoneList = []
        for run in queue["done"]:
            ok, newRun = ProjectUtil.get_queue_process(run, "done")
            newDoneList.append(newRun)
        newQueue = {"done": newDoneList, "work": newQueue["work"]}
    if len(queue["work"]) > 0:
        newWorkList = []
        for run in queue["work"]:
            ok, newRun = ProjectUtil.get_queue_process(run, "work")
            newWorkList.append(newRun)
        newQueue = {"done": newQueue["done"], "work": newWorkList}   
    return response(0, "success", newQueue)

@app.route('/get-model-information', methods=['POST'])
def get_model_information():
    '''
    get model information
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data:
        return response(1, "There is no data.")
    
    ok, projectPath = ProjectUtil.find_project(data["projectName"])
    if not ok:
        return response(1, projectPath)

    ok, deployPath = DeployUtil.get_deploy_path(projectPath)
    if not ok:
        deployPath = ""

    ok, deployInfo = DeployUtil.get_deploy_path_information(data["projectName"], deployPath)
    if not ok:
        deployInfo = {data['projectName']: []}

    ok, modelList = ProjectUtil.get_models(projectPath)
    if not ok:
        return response(1, modelList)
    newModelList = []
    for model in modelList:
        ok, newModel = ProjectUtil.get_queue_process(model, "model")
        newModelList.append(newModel)

    modelList = newModelList
    newModelList = []
    for model in modelList:
        ok, newModel = ProjectUtil.get_model_architecture(projectPath, model)
        newModelList.append(newModel)

    return response(0, "success", {
        'deployPath': deployPath,
        'deployInfo': deployInfo[data['projectName']],
        'modelList': newModelList,
    })

@app.route('/download-model/<string:header>/<string:payload>/<string:signature>', methods=['GET'])
def download_model(header, payload, signature):
    '''
    download model with filename setting
    '''
    jwt = f'{header}.{payload}.{signature}'
    ok, data = ProjectUtil.decode_key(jwt)
    print(data)
    if not ok or not data:
        return ('', 204)
    elif not 'projectName' in data or not 'runId' in data or not 'filename' in data:
        return ('', 204)
    
    ok, projectPath = ProjectUtil.find_project(data['projectName'])
    if not ok:
        return ('', 204)

    ok, onnxPath, onnxFile = DeployUtil.find_onnx(projectPath, data['runId'])
    if not ok:
        return ('', 204)
    print(onnxPath, onnxFile)

    return send_from_directory(onnxPath, onnxFile, download_name=f"{data['filename']}.onnx", as_attachment=True)

@app.route('/set-deploy-path', methods=['POST'])
def set_deploy_path():
    '''
    set deploy path
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'deployPath' in data:
        return response(1, "There is no data.")
    
    ok, projectPath = ProjectUtil.find_project(data["projectName"])
    if not ok:
        return response(1, projectPath)

    ok, info = DeployUtil.get_deploy_path_information(data["projectName"], data['deployPath'])
    if not ok:
        ok, deployPath = DeployUtil.get_deploy_path(projectPath)
        if not ok:
            return response(1, deployPath)

        ok, info = DeployUtil.get_deploy_path_information(data['projectName'], deployPath)
        if not ok:
            return response(1, info)
        return response(1, "Set deploy path failed", {
            'deployPath': deployPath,
            'info': info[data['projectName']]
        })

    ok = DeployUtil.set_deploy_path(projectPath, data['deployPath'])
    if not ok:
        ok, deployPath = DeployUtil.get_deploy_path(projectPath)
        if not ok:
            return response(1, deployPath)

        ok, info = DeployUtil.get_deploy_path_information(data['projectName'], deployPath)
        if not ok:
            return response(1, info)
        return response(1, "Set deploy path failed", {
            'deployPath': deployPath,
            'info': info[data['projectName']]
        })
    return response(0, "success", {
        'deployPath': data['deployPath'],
        'info': info[data['projectName']]
    })

@app.route('/deploy', methods=['POST'])
def deploy():
    '''
    deploy onnx to certain folder, and version control
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'runId' in data or not 'filename' in data:
        return response(1, "There is no data.")

    ok, projectPath = ProjectUtil.find_project(data["projectName"])
    if not ok:
        return response(1, projectPath)

    ok, result = DeployUtil.deploy(data["projectName"], projectPath, data['runId'], data['filename'])
    if not ok:
        return response(1, result)
    return response(0, "success", result[data['projectName']])

@app.route('/images/<path:path>', methods=['GET'])
def show_image(path):
    return send_from_directory(os.path.abspath(''), path=path)

# folder select and edit

@app.route('/list-dataset-folder', methods=['POST'])
def list_dataset_folder():
    folder = FolderUtil.list_folder('datasets')
    if folder == None:
        return response(1, "get dataset folder failed")
    return response(0, "success", folder)

@app.route('/create-dataset-folder', methods=['POST'])
def create_dataset_folder():
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'dir' in data:
        return response(1, "There is no data.")

    if FolderUtil.create_folder(os.path.join('datasets', data['root']), data['dir']):
        return response(0, "success")
    return response(1, "create datasets folder failed")

@app.route('/remove-dataset-folder', methods=['POST'])
def remove_dataset_folder():
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'dir' in data:
        return response(1, "There is no data.")

    if FolderUtil.remove_folder(os.path.join('datasets', data['root']), data['dir']):
        return response(0, "success")
    return response(1, "remove datasets folder failed")

@app.route('/rename-dataset-folder', methods=['POST'])
def rename_dataset_folder():
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'src' in data or not 'dst' in data:
        return response(1, "There is no data.")

    if FolderUtil.rename_folder(os.path.join('datasets', data['root']), data['src'], data['dst']):
        return response(0, "success")
    return response(1, "rename datasets folder failed")

@app.route('/list-deploy-folder', methods=['POST'])
def list_deploy_folder():
    folder = FolderUtil.list_folder('deploy')
    if folder == None:
        return response(1, "get deploy folder failed")
    return response(0, "success", folder)

@app.route('/create-deploy-folder', methods=['POST'])
def create_deploy_folder():
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'dir' in data:
        return response(1, "There is no data.")

    if FolderUtil.create_folder(os.path.join('deploy', data['root']), data['dir']):
        return response(0, "success")
    return response(1, "create deploys folder failed")

@app.route('/remove-deploy-folder', methods=['POST'])
def remove_deploy_folder():
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'dir' in data:
        return response(1, "There is no data.")

    if FolderUtil.remove_folder(os.path.join('deploy', data['root']), data['dir']):
        return response(0, "success")
    return response(1, "remove deploys folder failed")

@app.route('/rename-deploy-folder', methods=['POST'])
def rename_deploy_folder():
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'src' in data or not 'dst' in data:
        return response(1, "There is no data.")

    if FolderUtil.rename_folder(os.path.join('deploys', data['root']), data['src'], data['dst']):
        return response(0, "success")
    return response(1, "rename deploys folder failed")

# Experiment config
@app.route('/get-experiment-configs', methods=['POST'])
def get_experiment_configs():
    return response(0, "success", ExperimentConfig.config)

@app.route('/get-model-description', methods=['POST'])
def get_model_description():
    return response(0, "success", ModelDescription.modelDescription)

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
