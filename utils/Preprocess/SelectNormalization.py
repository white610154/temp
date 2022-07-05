import json
from datetime import datetime
from .NormalizeValueCalculate import get_std_mean


def load_dict_from_json(jsonFilePath):
    with open(jsonFilePath, 'r') as f:
        try:
            infoDict = json.load(f)
        except:
            raise BaseException('Something went wrong while loading normalizeRecord.json')
    return infoDict

def save_dict_to_json(jsonFilePath, infoDict):
    with open(jsonFilePath, 'w') as f:
        json.dump(infoDict, f, indent=4)


def set_normalize(PreprocessPara, task, normalization=None):
    jsonFilePath = f'./utils/Preprocess/normalizeRecord.json'

    if task is 'train':
        infoDict = load_dict_from_json(jsonFilePath)
        time = (datetime.now().strftime('%Y%m%d%H%M%S%f'))
        try:
            normalization = infoDict[PreprocessPara.normalize["mode"]]
        except:
            if isinstance(PreprocessPara.normalize["mean"], list) and isinstance(PreprocessPara.normalize["std"], list):
                normalization = {"mean": PreprocessPara.normalize["mean"], "std": PreprocessPara.normalize["std"]}
                key = PreprocessPara.normalize["mode"] if PreprocessPara.normalize["mode"] is not None else f'userInput_{time}'
                
            else:
                mean, std = get_std_mean(PreprocessPara.resize["imageSize"])
                normalization = {"mean": mean, "std": std}
                key = PreprocessPara.normalize["mode"] if PreprocessPara.normalize["mode"] is not None else f'autoCalculate_{time}'
            
            infoDict[key] = normalization
            save_dict_to_json(jsonFilePath, infoDict)
    
    elif task is 'test':
        infoDict = load_dict_from_json(jsonFilePath)
        try:
            normalization = infoDict[PreprocessPara.normalize["mode"]]

        except:
            if isinstance(PreprocessPara.normalize["mean"], list) and isinstance(PreprocessPara.normalize["std"], list):
                normalization = {"mean": PreprocessPara.normalize["mean"], "std": PreprocessPara.normalize["std"]}
            else:
                raise BaseException(f'Can not find "{PreprocessPara.normalize["mode"]}" normalization and got no input of maen and std.')
    
    return normalization