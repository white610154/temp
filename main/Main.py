from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import ProjectUtil

def response(code, message, data=None):
    # code=0 for success, code=1 for fail
    return {'code': code, 'message': message, 'data': data}

app = Flask(__name__)
CORS(app)

@app.route('/get-projects', methods=['POST'])
def get_projects():
    ok, projectList = ProjectUtil.get_projects()
    if not ok:
        return response(1, projectList)
    return response(0, "success", {'projects': projectList})

@app.route('/create-project-by-key', methods=['POST'])
def create_project_by_key():
    '''
    decode key to get config
    create a new project folder/ or already existed
    save config as json

    {
        "name": "aaaa",
        "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJDb25maWciOnsiUHJpdmF0ZVNldHRpbmciOnsiZGF0YXNldFBhdGgiOiIifX0sIkNvbmZpZ0F1Z21lbnRhdGlvbiI6eyJBdWdtZW50YXRpb25QYXJhIjp7InJhbmRvbUhvcml6b250YWxGbGlwIjp7InN3aXRjaCI6MSwicHJvYmFiaWxpdHkiOjAuNX19fSwiQ29uZmlnRXZhbHVhdGlvbiI6eyJFdmFsdWF0aW9uUGFyYSI6eyJzaG93QWNjIjoxLCJzaG93Q2xhc3NBY2MiOjF9fSwiQ29uZmlnTW9kZWxTZXJ2aWNlIjp7Ikxvc3NGdW5jdGlvblBhcmEiOnsibG9zc0Z1bmN0aW9uIjoiQ3Jvc3NFbnRyb3B5TG9zcyJ9LCJMZWFybmluZ1JhdGUiOnsibGVhcm5pbmdSYXRlIjowLjAwMX0sIk9wdGltaXplclBhcmEiOnsiQWRhbSI6eyJzd2l0Y2giOjEsImJldGFzIjpbMC45LDAuOTk5XSwiZXBzIjoxZS04LCJ3ZWlnaHREZWNheSI6MC4wMDA1LCJhbXNncmFkIjowfX0sIlNjaGVkdWxlclBhcmEiOnsic3RlcExSIjp7InN3aXRjaCI6MSwic3RlcFNpemUiOjEsImdhbW1hIjowLjV9fX0sIkNvbmZpZ1Bvc3Rwcm9jZXNzIjp7IlBvc3RQcm9jZXNzUGFyYSI6eyJjb25maWRlbmNlRmlsdGVyIjp7InN3aXRjaCI6MSwidGhyZXNob2xkIjowLjc1LCJzZWxlY3RMYWJlbCI6Ik9LIiwiY2xhc3NMaXN0IjpbIk5HIiwiT0siXX19fSwiQ29uZmlnUHJlcHJvY2VzcyI6eyJQcmVwcm9jZXNzUGFyYSI6eyJub3JtYWxpemUiOnsibW9kZSI6MH19fSwiQ29uZmlnUHl0b3JjaE1vZGVsIjp7IlNlbGVjdGVkTW9kZWwiOnsibW9kZWwiOnsic3RydWN0dXJlIjoiYXVvX21tZmFfbW9kZWwiLCJwcmV0cmFpbmVkIjoxfX0sIkNsc01vZGVsUGFyYSI6eyJiYXRjaFNpemUiOjE2LCJlcG9jaHMiOjJ9fX0.IYGFV0GmXV844ePMJw-jl_jJtNJjrWsQe0v0oDQB3ro"
    }
    '''
    data = request.get_json()
    if not data:
        return response(1, "There is no data.")

    ok, config = ProjectUtil.decode_key(data['key'])
    if not ok:
        return response(1, config)

    projectName = data['name']
    ok, projectList = ProjectUtil.create_project(projectName)
    if not ok:
        return response(1, projectList)

    ok, configPath = ProjectUtil.save_config_as_json(projectName, config)
    if not ok:
        return response(1, configPath)
    
    return response(0, "success", {"projects": projectList})

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
    
    found, projectPath = ProjectUtil.find_project(data['projectName'])
    if not found:
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

@app.route('/remote-dataset', methods=['POST'])
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
        ok, classList = ProjectUtil.check_data_labeled(f"{datasetPath}/train")

    status['labeled'] = ok

    found, projectPath = ProjectUtil.find_project(data['projectName'])
    if not found:
        return response(1, projectPath)
    ProjectUtil.add_dataset(projectPath, datasetPath, **status)

    return response(0, "success", status)

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
