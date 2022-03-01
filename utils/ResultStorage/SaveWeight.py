import os
import torch
from config.Config import BasicSetting, PrivateSetting

def save_model_weight(bestModel, weightName):
    """
    儲存當下最佳的權重

    Args:
        bestModel: 最佳模型
        savePath: 要儲存的路徑

    Output:
        BestWeight.pth: 準確率最佳的權重
    """
    if not os.path.isdir(PrivateSetting.outputPath):
        os.makedirs(PrivateSetting.outputPath)
    torch.save(bestModel.state_dict(), f'{PrivateSetting.outputPath}/{weightName}.pth')
