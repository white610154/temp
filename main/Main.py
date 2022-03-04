from flask import Flask, jsonify, request
from flask_cors import CORS
import utils.CryptoUtil

app = Flask(__name__)
CORS(app)

@app.route('/creat-project-by-key', methods=['POST'])
def create_project_by_key():
    '''
    decode key to get config
    create a new project folder/ or already existed
    save config as json
    '''
    data = request.get_json()
    if not data:
        return "There is no data."

    projectName = data['name']
    config = utils.CryptoUtil.decode_key(data['key'])
    if not config:
        return "Wrong key format."

    projectsList = utils.CryptoUtil.create_project(projectName)
    if not projectsList:
        return "Invalid project name."
    
    configPath = utils.CryptoUtil.save_config_as_json(projectName, config)
    if not configPath:
        return "Config save error."
    
    return {"projects": projectsList}

@app.route('/get-experiments', methods=['POST'])
def get_experiments():
    '''
    return experiment config
    '''
    data = request.get_json()
    if not data:
        return "There is no data."
    
    projectName = data['name']
    projectFolderPath = utils.CryptoUtil.find_project(projectName)
    if not projectFolderPath:
        return "Project does not exist."
    elif projectFolderPath == False:
        return "Project does not exist."

    config = utils.CryptoUtil.get_config(projectFolderPath)

    return config


@app.route('/check-dataset', methods=['POST'])
def check_dataset():
    '''
    check dataset status: {uploaded: bool, labeled: bool, split: bool}
    '''
    data = request.get_json()
    if not data:
        return "There is no data."

    return data

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()