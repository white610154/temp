import torch.nn as LossFunctionMethod
from config.ConfigModelService import LossFunctionPara

def select_loss_function():
    method = getattr(LossFunctionMethod, LossFunctionPara.lossFunction)
    lossFunction = method()

    return lossFunction