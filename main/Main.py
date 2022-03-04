from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.CryptoUtil import decode_key, make_project_folder, save_config_as_json

app = Flask(__name__)
CORS(app)

@app.route('/creat-project-by-key', methods=['POST'])
def create_project_by_key():
    data = request.get_json()
    if not data:
        return "There is no data."

    projectName = data['name']
    config = decode_key(data['key'])
    if not config:
        return "Wrong key format."

    projectsList = make_project_folder(projectName)
    if not projectsList:
        return "Invalid project name."
    
    configPath = save_config_as_json(projectName, config)
    if not configPath:
        return "Config save error."

    

    # create project folder projects/{{projectName}}/experiments/202203021355.json
    # decode solution key and save experiment config
    # return jsonify(config)

    
    return jsonify(projectsList)

@app.route('/get-experiments', methods=['POST'])
def get_experiments():
    # return experiments config
    return ''

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()