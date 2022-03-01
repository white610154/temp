from config.ConfigResultStorage import ResultStorage
from config.ConfigPytorchModel import ClsModelPara
from utils.ResultStorage import SaveWeight

def save_weight(model, bestAcc, currentAcc, epoch):
    if bestAcc <= currentAcc:
        bestAcc = currentAcc
        SaveWeight.save_model_weight(model, 'BestWeight')

    if ResultStorage.saveFinalWeight and epoch + 1 == ClsModelPara.epochs:
        SaveWeight.save_model_weight(model, 'FinalWeight')

    if ResultStorage.saveCheckpoint['switch'] and (epoch + 1) % ResultStorage.saveCheckpoint['saveIter'] == 0:
        SaveWeight.save_model_weight(model, 'CheckPoint')
        
    return bestAcc
