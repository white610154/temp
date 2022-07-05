import torch, math
from utils import AiModel
from config.ConfigPytorchModel import SelectedModel, ClsPath, ClsModelPara
from config.Config import BasicSetting
from distutils.version import LooseVersion
import os

def check_input_size(imgSize, modelName, structureList, checkSize):
    width, height = imgSize[0], imgSize[1]
    for layer in structureList:
        width = math.ceil((width + 2 * layer[2] - layer[0] + 1) / layer[1])
        height = math.ceil((height + 2 * layer[2] - layer[0] + 1) / layer[1])
    if (width % checkSize != 0) or (height % checkSize != 0):
        raise ValueError(f'Please set resize["switch"]: True and resize["imageSize"]: [224, 244] in config/ConfigPreprocess to make sure that {modelName} model can be packed correctly.')

def select_model(imgSize:list=[224, 224]):
    """
    Selecting model and loading the pretrained weight according to ConfigPytorchModel.

    Return:
        model
    """
    # check if the vgg, alexnet model can be pack into Onnx
    if SelectedModel.model["structure"].startswith('vgg'):
        structureList = [[3, 1, 1], [3, 1, 1], [2, 2, 0],
                        [3, 1, 1], [3, 1, 1], [2, 2, 0], 
                        [3, 1, 1], [3, 1, 1], [3, 1, 1],
                        [2, 2, 0], [3, 1, 1], [3, 1, 1],
                        [3, 1, 1], [2, 2, 0], [3, 1, 1],
                        [3, 1, 1], [3, 1, 1], [2, 2, 0]]
        check_input_size(imgSize, SelectedModel.model["structure"], structureList, 7)
    
    elif SelectedModel.model["structure"].startswith('alexnet'):
        structureList = [[11, 4, 2], [3, 2, 0], [5, 1, 2], [3, 2, 0],
                        [3, 1, 1], [3, 1, 1], [3, 1, 1], [3, 2, 0]]
        check_input_size(imgSize, SelectedModel.model["structure"], structureList, 6)

    if SelectedModel.model["structure"].startswith('efficientnet'):
        if LooseVersion(torch.__version__) < LooseVersion('1.10.0'):
            raise BaseException(f'efficientnet needs torch version >= 1.10.0. But the torch version is {torch.__version__}.')
        else:
            from utils.AiModel import efficientnet
            method = getattr(efficientnet, SelectedModel.model["structure"])
            model = method(pretrained=SelectedModel.model["pretrained"])
    
    elif SelectedModel.model["structure"] == 'CustomModel':
        model = None
    
    else:
        method = getattr(AiModel, SelectedModel.model["structure"])
        model = method(pretrained=SelectedModel.model["pretrained"])
    
    model = load_model_weight(model, BasicSetting.task, SelectedModel.model["pretrained"])
    return model


def load_model_weight(model, task, pretrained):
    """
    According to different task (Train / Test / Inference), load the model weight

    Return:
        model with weight.
    """
    if task == 'Train':
        if SelectedModel.model["structure"] == 'CustomModel':
            raise ValueError(f'CustomModel can only used for "Retrain" task')
        
        elif not pretrained:
            pass

        elif SelectedModel.model["pretrained"] and not os.path.isfile(ClsPath.pretrainedWeight):       # check pretrianed Weight exists
            raise ValueError(f'No pre-trained weight is available for model type {SelectedModel.model["structure"]}')   
            
        elif SelectedModel.model["pretrained"] and not SelectedModel.model["structure"].startswith('densenet'): 
            model.load_state_dict(torch.load(ClsPath.pretrainedWeight), strict=True)
    
    elif task == 'Retrain':
        if SelectedModel.model["structure"] == 'CustomModel':
            model = torch.jit.load(ClsPath.customModel)
        else:
            model.load_state_dict(torch.load(ClsPath.customModel), strict=False)

    else:
        if SelectedModel.model["structure"] == 'CustomModel':
            model = torch.jit.load(ClsPath.weightPath)
        else:
            model.load_state_dict(torch.load(ClsPath.weightPath), strict=False)
        
    return model
