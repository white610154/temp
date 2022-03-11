from config.ConfigResultStorage import ResultStorage
from config.ConfigPytorchModel import ClsModelPara
from utils.ResultStorage import SaveWeight

def save_weight(model, bestAcc, currentAcc, epoch):
    """
    According to configs in ConfigResultStorage, save different model weight.

    Args:
        model: whole model
        bestAcc: best accuracy till now
        currentAcc: accuracy of the current epoch
        epoch: current epoch number
    Return:
        bestAcc: update best accuracy till now and return
    """
    if bestAcc <= currentAcc:
        bestAcc = currentAcc
        SaveWeight.save_model_weight(model, 'BestWeight')

    if ResultStorage.saveFinalWeight and epoch + 1 == ClsModelPara.epochs:
        SaveWeight.save_model_weight(model, 'FinalWeight')

    if ResultStorage.saveCheckpoint['switch'] and (epoch + 1) % ResultStorage.saveCheckpoint['saveIter'] == 0:
        SaveWeight.save_model_weight(model, 'CheckPoint')
        
    return bestAcc
