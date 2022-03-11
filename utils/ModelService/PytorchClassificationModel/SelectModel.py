import torch
from utils import AiModel
from config.ConfigPytorchModel import SelectedModel, ClsPath
from distutils.version import LooseVersion
import os

def select_model():
    """
    Selecting model and loading the pretrained weight according to ConfigPytorchModel.

    Return:
        model
    """
    if SelectedModel.model['structure'].startswith('efficientnet'):
        if LooseVersion(torch.__version__) < LooseVersion('1.10.0'):
            raise BaseException(f"efficientnet needs torch version >= 1.10.0. But the torch version is {torch.__version__}.")
        else:
            from utils.AiModel import efficientnet
            method = getattr(efficientnet, SelectedModel.model['structure'])
    else:
        method = getattr(AiModel, SelectedModel.model['structure'])
   
    model = method(pretrained=SelectedModel.model['pretrained']) 
    
    if SelectedModel.model['pretrained'] and not os.path.isfile(ClsPath.pretrainedWeight):       # check pretrianed Weight exists
        raise ValueError(f"No pre-trained weight is available for model type {SelectedModel.model['structure']}")   
        
    if SelectedModel.model['pretrained'] and not SelectedModel.model['structure'].startswith('densenet'): 
        model.load_state_dict(torch.load(ClsPath.pretrainedWeight), strict=True)  

    return model