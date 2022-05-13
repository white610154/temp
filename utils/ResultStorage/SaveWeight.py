import os
import torch
import pickle
from config.Config import PrivateSetting

def create_folder(folderPath=PrivateSetting.outputPath):
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath)


def save_weight(model, weightName):
    """
    Save the weight of model for inference phase.

    Args:
        model: the entire model
        weightName: the saved weight file name
    Output:
        xxx.pth: the weight file of model
    """
    torch.save(model.state_dict(), f'{PrivateSetting.outputPath}/{weightName}.pth')


def save_model_optimizer(model, optimizer, weightName):
    """
    Save the entire model and optimizer for keep training.

    Args:
        model: the entire model
        optimizer: the entire optimizer
        weightName: the saved weight file name
    Output:
        xxx_model.pth: model include structure and parameter
        xxx_optimizer.pth: optimizer include structure and parameter
    """
    state = {'model': model, 'optimizer':optimizer}  
    torch.save(state, f'{PrivateSetting.outputPath}/whole_checkpoint.pth')
    # config = {"model": model, "optim": optimizer}
    # with open(f'{PrivateSetting.outputPath}/whole_checkpoint.pickle', 'wb') as f:
    #     pickle.dump(config, f)
