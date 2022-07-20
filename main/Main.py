from datetime import datetime
import os
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from utils import ProjectUtil
from utils.ProjectUtil import DeployUtil, ExperimentConfig, FolderUtil, ModelDescription
from main import LoggerConfig
from utils.EasyAuth import EasyAuthService, Auth, User

LoggerConfig.set_logger_config()

def response(code, message, data=None):
    # code=0 for success, code=1 for fail
    return {'code': code, 'message': message, 'data': data}

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
CORS(app)

def check_auth(auth: str):
    '''
    Check user auth, check project auth if projectName in body
    '''
    def wrapper(func):
        def func_with_auth(*args, **kwargs):
            user = None
            try:
                token = request.headers.get('Authorization')
                if token.startswith('Bearer'):
                    token = token[7:]
                else:
                    return response(1, "Authorized failed")
                user = EasyAuthService.authorize(token)
                if auth != None:
                    data = request.get_json()
                    authorized = EasyAuthService.check_auth(user.username, auth, data.get('projectName'))
                    if not authorized:
                        return response(1, "Authorized failed")
            except Exception as err:
                print(err)
                return response(1, "Authorized failed")
            return func(user, *args, **kwargs)
        setattr(func_with_auth, '__name__', func.__name__)
        return func_with_auth
    return wrapper

### project

@app.route('/create-project-by-key', methods=['POST'])
@check_auth(Auth.maintainer)
def create_project_by_key(user: User):
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

    EasyAuthService.add_group(data['name'], user.username)

    ok, configPath = ProjectUtil.save_config_as_json(data['name'], config)
    if not ok:
        return response(1, configPath)

    ok, projectList = ProjectUtil.get_projects()
    if not ok:
        return response(1, projectList)
    
    return response(0, "success", {"projects": projectList})

@app.route('/remove-project', methods=['POST'])
@check_auth(Auth.admin)
def remove_projects(user: User):
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

    ok, msg = ProjectUtil.delete_run_in_queue(data["projectName"], 'All')
    if not ok:
        return response(1, msg)
    
    ok, message = ProjectUtil.delete_project(projectPath)
    if not ok:
        return response(1, message)
    
    EasyAuthService.remove_group(data['projectName'])

    ok, projectList = ProjectUtil.get_projects()
    if not ok:
        return response(1, projectList)
    
    return response(0, "success", {'projects': projectList})

@app.route('/get-projects', methods=['POST', 'GET'])
@check_auth(Auth.user)
def get_projects(user: User):
    '''
    input: / output: projectList
    '''
    ok, projectList = ProjectUtil.get_projects()
    if not ok:
        return response(1, projectList)

    projectList = [
        project
        for project in projectList
        if EasyAuthService.group(project).auth_of(user.username) != None
    ]

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
@check_auth(Auth.user)
def get_experiments(user: User):
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
@check_auth(Auth.user)
def set_experiments(user: User):
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
@check_auth(Auth.user)
def check_dataset(user: User):
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
@check_auth(Auth.owner)
def remove_dataset(user: User):
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
@check_auth(Auth.user)
def get_datasets(user: User):
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
@check_auth(Auth.user)
def set_experiment_dataset(user: User):
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
@check_auth(Auth.user)
def run_experiment_train(user: User):
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
@check_auth(Auth.user)
def run_experiment_test(user: User):
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
@check_auth(Auth.user)
def remove_run_in_queue(user: User):
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
@check_auth(Auth.owner)
def remove_run(user: User):
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
@check_auth(Auth.user)
def get_queue_information(user: User):
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
@check_auth(Auth.user)
def get_model_information(user: User):
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
@check_auth(Auth.user)
def download_model(user: User, header, payload, signature):
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
@check_auth(Auth.owner)
def set_deploy_path(user: User):
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
@check_auth(Auth.user)
def deploy(user: User):
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
@check_auth(Auth.user)
def show_image(user: User, path):
    return send_from_directory(os.path.abspath(''), path=path)

# folder select and edit

@app.route('/list-dataset-folder', methods=['POST'])
@check_auth(Auth.user)
def list_dataset_folder(user: User):
    folder = FolderUtil.list_folder('datasets')
    if folder == None:
        return response(1, "get dataset folder failed")
    return response(0, "success", folder)

@app.route('/create-dataset-folder', methods=['POST'])
@check_auth(Auth.maintainer)
def create_dataset_folder(user: User):
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'dir' in data:
        return response(1, "There is no data.")

    if FolderUtil.create_folder(os.path.join('datasets', data['root']), data['dir']):
        return response(0, "success")
    return response(1, "create datasets folder failed")

@app.route('/remove-dataset-folder', methods=['POST'])
@check_auth(Auth.maintainer)
def remove_dataset_folder(user: User):
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'dir' in data:
        return response(1, "There is no data.")

    if FolderUtil.remove_folder(os.path.join('datasets', data['root']), data['dir']):
        return response(0, "success")
    return response(1, "remove datasets folder failed")

@app.route('/rename-dataset-folder', methods=['POST'])
@check_auth(Auth.maintainer)
def rename_dataset_folder(user: User):
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'src' in data or not 'dst' in data:
        return response(1, "There is no data.")

    if FolderUtil.rename_folder(os.path.join('datasets', data['root']), data['src'], data['dst']):
        return response(0, "success")
    return response(1, "rename datasets folder failed")

@app.route('/list-deploy-folder', methods=['POST'])
@check_auth(Auth.user)
def list_deploy_folder(user: User):
    folder = FolderUtil.list_folder('deploy')
    if folder == None:
        return response(1, "get deploy folder failed")
    return response(0, "success", folder)

@app.route('/create-deploy-folder', methods=['POST'])
@check_auth(Auth.maintainer)
def create_deploy_folder(user: User):
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'dir' in data:
        return response(1, "There is no data.")

    if FolderUtil.create_folder(os.path.join('deploy', data['root']), data['dir']):
        return response(0, "success")
    return response(1, "create deploys folder failed")

@app.route('/remove-deploy-folder', methods=['POST'])
@check_auth(Auth.maintainer)
def remove_deploy_folder(user: User):
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'dir' in data:
        return response(1, "There is no data.")

    if FolderUtil.remove_folder(os.path.join('deploy', data['root']), data['dir']):
        return response(0, "success")
    return response(1, "remove deploys folder failed")

@app.route('/rename-deploy-folder', methods=['POST'])
@check_auth(Auth.maintainer)
def rename_deploy_folder(user: User):
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'root' in data or not 'src' in data or not 'dst' in data:
        return response(1, "There is no data.")

    if FolderUtil.rename_folder(os.path.join('deploy', data['root']), data['src'], data['dst']):
        return response(0, "success")
    return response(1, "rename deploys folder failed")

# Experiment config
@app.route('/get-experiment-configs', methods=['POST'])
@check_auth(Auth.user)
def get_experiment_configs(user: User):
    return response(0, "success", ExperimentConfig.config)

@app.route('/get-model-description', methods=['POST'])
@check_auth(Auth.user)
def get_model_description(user: User):
    return response(0, "success", ModelDescription.modelDescription)

@app.route('/get-model-pretrained-weight', methods=['POST'])
@check_auth(Auth.user)
def get_model_pretrained_weight(user: User):
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'model' in data:
        return response(1, "There is no data.")

    ok, modelId = ProjectUtil.transfer_model(data["model"])
    if not ok:
        return response(1, modelId)
    
    ok, pretrainedWeightPath = ProjectUtil.find_pretrained_weight(modelId)

    return response(0, "success", hasPretrainedWeight(data['model']))

# login and auth system

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'username' in data or not 'password' in data:
        return response(1, "There is no data.")

    user = EasyAuthService.login(data['username'], data['password'])
    token = user.generate_token(datetime.now())
    return response(0, "success", token)

@app.route('/users/all', methods=['POST'])
@check_auth(Auth.admin)
def get_users(user: User):
    users = {
        'users': [user.username for user in EasyAuthService.users if user != None],
        'maintainers': [
            user
            for user, auth in EasyAuthService.group("_all_").auths.items()
            if auth == Auth.maintainer
        ]
    }
    return response(0, "success", users)

@app.route('/users/project', methods=['POST'])
@check_auth(Auth.owner)
def get_project_users(user: User):
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data:
        return response(1, "There is no data.")

    group = EasyAuthService.group(data['projectName'])
    if group.name == 'Unknown':
        return response(1, "Project auth settings not found")

    users = {
        'users': [user.username for user in EasyAuthService.users if user != None],
        'members': group.auths
    }
    return response(0, "success", users)

@app.route('/add-user', methods=['POST'])
@check_auth(Auth.admin)
def add_user(user: User):
    '''
    Add user to login system, return userId and return 0 for add user failed.
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'username' in data or not 'password' in data or not 'maintainer' in data:
        return response(1, "There is no data.")

    userId = EasyAuthService.add_user(data['username'], data['password'], data['maintainer'])
    return response(0, "success", userId)

@app.route('/remove-user', methods=['POST'])
@check_auth(Auth.admin)
def remove_user(user: User):
    '''
    Remove user from login system, return userId and return 0 for add user failed.
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'username' in data:
        return response(1, "There is no data.")

    EasyAuthService.remove_user(data['username'])
    return response(0, "success", None)

@app.route('/modify-user', methods=['POST'])
@check_auth(Auth.admin)
def modify_user(user: User):
    '''
    Modify user information
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'isMaintainer' in data:
        return response(1, "There is no data.")

    if data['isMaintainer']:
        EasyAuthService.group('_all_').add_user(user.username, Auth.maintainer)
    else:
        EasyAuthService.group('_all_').remove_user(user.username)
    return response(0, "success", None)

@app.route('/add-project-user', methods=['POST'])
@check_auth(Auth.owner)
def add_project_user(user: User):
    '''
    Add user to project and set auth to user
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'username' in data or not 'projectName' in data or not 'auth' in data:
        return response(1, "There is no data.")

    group = EasyAuthService.group(data['projectName'])
    if group.name == 'Unknown':
        return response(1, "Project auth settings not found")
    group.add_user(data['username'], data['auth'])
    return response(0, "success")

@app.route('/remove-project-user', methods=['POST'])
@check_auth(Auth.owner)
def remove_project_user(user: User):
    '''
    Add user to project and set auth to user
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'username' in data or not 'projectName' in data or not 'auth' in data:
        return response(1, "There is no data.")

    group = EasyAuthService.group(data['projectName'])
    if group.name == 'Unknown':
        return response(1, "Project auth settings not found")
    group.remove_user(data['username'])
    return response(0, "success")

@app.route('/modify-project-user', methods=['POST'])
@check_auth(Auth.owner)
def modify_project_user(user: User):
    '''
    Modify user information
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'username' in data or not 'auth' in data:
        return response(1, "There is no data.")

    group = EasyAuthService.group(data['projectName'])
    if group.name == 'Unknown':
        return response(1, "Project auth settings not found")
    group.add_user(data['username'], data['auth'])
    return response(0, "success", None)

@app.route('/change-password', methods=['POST'])
@check_auth(None)
def change_password(user: User):
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'password' in data:
        return response(1, "There is no data.")

    userId = EasyAuthService.change_password(user.username, data['password'])
    if userId == 0:
        return response(1, "user not found")

    return response(0, "success", userId)

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
