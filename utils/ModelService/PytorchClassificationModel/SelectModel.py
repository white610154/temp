import torch
from utils.AiModel import ModelStructure
from config.ConfigPytorchModel import SelectedModel, ClsPath


def select_model():
    if SelectedModel.model['structure'].split('_')[0] == 'efficientnet':
        if torch.__version__ > '1.10.0':
            raise BaseException(f"efficientnet needs torch version >= 1.10.0. But the torch version is {torch.__version__}.")
    
    method = getattr(ModelStructure, SelectedModel.model['structure'])
    model = method()
    if SelectedModel.model['pretrained']:
        model.load_state_dict(torch.load(ClsPath.pretrainedWeight), strict=False)  

    return model