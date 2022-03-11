import torch.nn as LossFunctionMethod
from config.ConfigModelService import LossFunctionPara

def select_loss_function():
    """
    Select loss functcion from torch.nn module.

    Return:
        lossFunction
    """
    method = getattr(LossFunctionMethod, LossFunctionPara.lossFunction)
    lossFunction = method()

    return lossFunction