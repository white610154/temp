from utils.ResultStorage.SaveOnnxModel import onnx_pack
from config.ConfigResultStorage import ResultStorage
from config.ConfigPytorchModel import ClsModelPara
from utils.ResultStorage import SaveWeight, SaveAcc, TestAcc

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
        if ResultStorage.saveOnnxModel["switch"]:
            onnx_pack(model=model, packageName=ResultStorage.saveOnnxModel["fileName"])


    if ResultStorage.saveFinalWeight["switch"] and epoch + 1 == ClsModelPara.epochs:
        SaveWeight.save_model_weight(model, 'FinalWeight')

    if ResultStorage.saveCheckpoint['switch'] and (epoch + 1) % ResultStorage.saveCheckpoint["saveIter"] == 0:
        SaveWeight.save_model_weight(model, 'CheckPoint')
        
    return bestAcc


def save_acc(epoch:int, total:int, totalCorrect:int, classTotal:list, classCorrect:list, className:list):
    if ResultStorage.saveAccTxt["switch"]:
        SaveAcc.save_epoch_acc_txt(epoch, total, totalCorrect, classTotal, classCorrect, className)
    
    if ResultStorage.saveAccJson["switch"]:
        SaveAcc.save_epoch_acc_json(epoch, ClsModelPara.epochs, total, totalCorrect)

def test_acc(totalCorrect:int, classTotal:list, classCorrect:list):
    if ResultStorage.testAccJson["switch"]:
        TestAcc.test_epoch_acc_json(classTotal, classCorrect)