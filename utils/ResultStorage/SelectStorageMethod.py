from config.ConfigResultStorage import ResultStorage
from config.ConfigPostprocess import PostProcessPara
from config.ConfigPytorchModel import ClsModelPara
from utils.ResultStorage import SaveWeight, SaveResult

def save_result(resultList:list, classNameList:list, outputPath:str, task:str) -> None:
    """
    output prediction for 3 types as csv file

    Args:
        resultList: whole model
        classNameList: optimizer use for training
        outputPath: best accuracy till now
        task: accuracy of the current epoch
    """
    classNameList.sort()
    classNameList.sort(key=lambda x:x)
    for count, result in enumerate(resultList):
        if PostProcessPara.unknownFilter["switch"] and PostProcessPara.unknownFilter["saveCsvMode"] > 0:
            SaveResult.ResultCsv(result, count, task, outputPath, classNameList,
                                 unknownMode=PostProcessPara.unknownFilter["saveCsvMode"]).write_unknown()
        if ResultStorage.savePredictResult["switch"]:
            SaveResult.ResultCsv(result, count, task, outputPath, classNameList).write_result()

        if ResultStorage.saveWrongFile["switch"] and task == 'Test':
            SaveResult.ResultCsv(result, count, task, outputPath, classNameList).write_wrong()

def save_model(modelType, model, optimizer, cudaDevice, bestAcc:float, currentAcc:float, epoch:int):
    ### 阿阿阿世亞對不起這個還給你了
    """
    According to configs in ConfigResultStorage, save different model weight.

    Args:
        model: whole model
        optimizer: optimizer use for training
        bestAcc: best accuracy till now
        currentAcc: accuracy of the current epoch
        epoch: current epoch number
    Return:
        bestAcc: update best accuracy till now and return
    """
    if bestAcc <= currentAcc:
        bestAcc = currentAcc
        if ResultStorage.saveBestDictPth["switch"]:
            if modelType is not 'CustomModel':
                SaveWeight.save_weight(model, 'BestDictPth')
            else:
                print('Warning: CustomModel(ScriptPth) is not supported DictPth model saving')
        if ResultStorage.saveBestScriptPth["switch"]:
            SaveWeight.save_script_model(model, 'BestScriptPth')
        if ResultStorage.saveBestOnnx["switch"]:
            try:
                SaveWeight.onnx_pack(model, cudaDevice, 'BestOnnx')
            except:
                if modelType is 'CustomModel':
                    print('Warning: CustomModel(ScriptPth) can not save as onnx model')
                else:
                    print('Warning: The official onnx module have not supported mobilenet(Hardswish) packing')

    if ResultStorage.saveCheckpoint["switch"] and (epoch + 1) % ResultStorage.saveCheckpoint["saveIter"] == 0:
        SaveWeight.save_model_optimizer(epoch, model, optimizer, 'CheckPoint')

    if epoch + 1 == ClsModelPara.epochs:
        if ResultStorage.saveFinalDictPth["switch"]:
            if modelType is not 'CustomModel':
                SaveWeight.save_weight(model, 'FinalDictPth')
            else:
                print('Warning: CustomModel(ScriptPth) is not supported DictPth model saving')
        if ResultStorage.saveFinalScriptPth["switch"]:
            SaveWeight.save_script_model(model, 'FinalScriptPth')
        if ResultStorage.saveFinalOnnx["switch"]:
            try:
                SaveWeight.onnx_pack(model, cudaDevice, 'FinalOnnx')
            except:
                if modelType is 'CustomModel':
                    print('Warning: CustomModel(ScriptPth) can not save as onnx model')
                else:
                    print('Warning: The official onnx module have not supported mobilenet(Hardswish) packing')
        
    return bestAcc