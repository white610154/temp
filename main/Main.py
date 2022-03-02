from flask import Flask, jsonify, request
from flask_cors import CORS

import jwt

key = '2c3d60951d544a8bf815c1b8485047da793d395fbee26c63c4f0f6c3d1d3ebe6'
algorithm = 'HS256'

def decode(token):
    deDict = jwt.decode(token, key, algorithms=[algorithm])
    return deDict

app = Flask(__name__)
CORS(app)

@app.route('/creat-project-by-key', methods=['POST'])
def create_project_by_key():
    data = request.get_json()
    # create project folder projects/{{projectName}}/experiments/202203021355.json
    # decode solution key and save experiment config
    config = decode(data['key'])
    return jsonify(config)

@app.route('/get-experiments', methods=['POST'])
def get_experiments():
    # return experiments config
    return ''

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()