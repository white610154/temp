from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from utils import ProjectUtil

def response(code, message, data=None):
    # code=0 for success, code=1 for fail
    return {'code': code, 'message': message, 'data': data}

app = Flask(__name__)
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

@app.route('/delete-project', methods=['POST'])
def delete_projects():
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
    ok, projectList = ProjectUtil.get_projects()
    if not ok:
        return response(1, projectList)

    return response(0, "success", {'projects': projectList})

@app.route('/check-project', methods=['POST'])
def check_projects():
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
    return experiment config
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    
    projectName = data['projectName']
    ok, projectPath = ProjectUtil.find_project(projectName)
    if not ok:
        return response(1, projectPath)

    ok, config = ProjectUtil.get_config(projectPath)
    if not ok:
        return response(1, config)

    return response(0, "success", config)

@app.route('/set-experiment-dataset', methods=['POST'])
def set_experiment_dataset():
    '''
    set dataset of experiment
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'experimentId' in data or not 'datasetPath' in data:
        return response(1, "There is no data.")
    
    ok, projectPath = ProjectUtil.find_project(data['projectName'])
    if not ok:
        return response(1, projectPath)

    ok, config = ProjectUtil.set_config_dataset(projectPath, data['experimentId'], data['datasetPath'])
    if not ok:
        return response(1, config)
    return response(0, "success", config)

@app.route('/get-datasets', methods=['POST'])
def get_datasets():
    '''
    get datasets of project
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data:
        return response(1, "There is no data.")

    found, projectPath = ProjectUtil.find_project(data['projectName'])
    if not found:
        return response(1, projectPath)

    datasets = ProjectUtil.get_datasets(projectPath)
    if not datasets:
        return response(1, "read file error")
    return response(0, "success", datasets)

@app.route('/remove-dataset', methods=['POST'])
def remove_dataset():
    '''
    remove dataset from project
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'datasetPath' in data:
        return response(1, "There is no data.")

    found, projectPath = ProjectUtil.find_project(data['projectName'])
    if not found:
        return response(1, projectPath)

    datasets = ProjectUtil.remove_dataset(projectPath)
    if not datasets:
        return response(1, "write file error")
    return response(0, "success", datasets)

@app.route('/check-dataset', methods=['POST'])
def check_dataset():
    '''
    check dataset status: {uploaded: bool, labeled: bool, split: bool}
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'datasetPath' in data or not 'projectName' in data:
        return response(1, "There is no data.")

    status = {
        'uploaded': False,
        'labeled': False,
        'split': False,
    }

    datasetPath = data['datasetPath']
    ok, dataList = ProjectUtil.check_data_uploaded(datasetPath)
    if not ok:
        return response(1, dataList)
    status['uploaded'] = True

    ok, datasetList = ProjectUtil.check_data_split(datasetPath)
    if not ok:
        status['split'] = False
        ok, classList = ProjectUtil.check_data_labeled(datasetPath)
    elif ok:
        status['split'] = True
        ok, classList = ProjectUtil.check_data_labeled(f"{datasetPath}/Train")

    status['labeled'] = ok

    found, projectPath = ProjectUtil.find_project(data['projectName'])
    if not found:
        return response(1, projectPath)
    ProjectUtil.add_dataset(projectPath, datasetPath, **status)

    return response(0, "success", status)

@app.route('/run-experiment-train', methods=['POST'])
def run_experiment_train():
    '''
    run experiment
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'experimentId' in data:
        return response(1, "There is no data.")
    ok, msg = ProjectUtil.save_run_in_queue(data, task="Train")
    if not ok:
        return response(1, msg)
    return response(0, "success", msg)

@app.route('/get-information-train', methods=['POST'])
def get_information_train():
    '''
    get information
    '''
    ok, runs = ProjectUtil.get_runs()
    if not ok:
        return response(1, runs)
    if len(runs["done"]) <= 0 and len(runs["work"]) <= 0:
        return response(1, runs)
    newRuns = {"done": runs["done"], "work": runs["work"]}
    if len(runs["done"]) > 0:
        newDoneList = []
        for run in runs["done"]:
            ok, newRun = ProjectUtil.get_queue_process(run, "done")
            newDoneList.append(newRun)
        newRuns = {"done": newDoneList, "work": newRuns["work"]}
    if len(runs["work"]) > 0:
        newWorkList = []
        for run in runs["work"]:
            ok, newRun = ProjectUtil.get_queue_process(run, "work")
            newWorkList.append(newRun)
        newRuns = {"done": newRuns["done"], "work": newWorkList}   
    return response(0, "success", newRuns)

@app.route('/delete-run', methods=['POST'])
def delete_run():
    '''
    delete run
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

@app.route('/run-experiment-test', methods=['POST'])
def run_experiment_test():
    '''
    run experiment
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")
    elif not 'projectName' in data or not 'experimentId' in data or not 'runId' in data:
        return response(1, "There is no data.")
    ok, msg = ProjectUtil.save_run_in_queue(data, task="Test")
    if not ok:
        return response(1, msg)
    return response(0, "success", msg)

@app.route('/download-model/<string:header>/<string:payload>/<string:signature>', methods=['GET'])
def download_model(header, payload, signature):
    '''
    download model with filename setting
    '''
    jwt = f'{header}.{payload}.{signature}'
    ok, data = ProjectUtil.decode_key(jwt)
    print(data)
    if not ok or not data:
        return response(1, "There is no data")
    elif not 'projectName' in data or not 'runId' in data or not 'filename' in data:
        return response(1, "There is no data")
    
    ok, projectPath = ProjectUtil.find_project(data['projectName'])
    if not ok:
        return response(1, projectPath)

    ok, onnxPath = ProjectUtil.find_onnx(projectPath, data['runId'])
    if not ok:
        return response(1, onnxPath)
    print(onnxPath)

    return send_file(onnxPath, download_name=f"{data['filename']}.onnx")

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
