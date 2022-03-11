import os
import torch
from config.Config import BasicSetting, PrivateSetting

def save_model_weight(model, weightName):
    """
    Save the weight of model.

    Args:
        model: the entire model
        weightName: the saved weight file name

    Output:
        xxx.pth: the weight file of model
    """
    if not os.path.isdir(PrivateSetting.outputPath):
        os.makedirs(PrivateSetting.outputPath)
    torch.save(model.state_dict(), f'{PrivateSetting.outputPath}/{weightName}.pth')
