from config.Config import PrivateSetting

class SelectedModel:
    model = {'structure': '', 'pretrained': False}

class ClsModelPara:
    cudaDevice = 3
    batchSize = 1
    epochs = 1

class ClsPath:
    trainPath = f'./{PrivateSetting.datasetPath}/Train'
    validPath = f'./{PrivateSetting.datasetPath}/Valid'
    testPath = f'./{PrivateSetting.datasetPath}/Test'
    inferencePath = f'./{PrivateSetting.datasetPath}/Inference'
    pretrainedWeight = f'./sample/PretrainedWeight/{SelectedModel.model["structure"]}.pth'
    weightPath = f'./{PrivateSetting.outputPath}/BestDictPth.pth'
    customModel = f'./sample/CustomModel/CustomScriptPth.pth'