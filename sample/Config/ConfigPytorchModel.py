from config.Config import PrivateSetting

class SelectedModel:
    model            = {'structure': 'regnet_y_400mf', 'pretrained': True}

class ClsModelPara:
    cudaDevice       = 2
    batchSize        = 16
    epochs           = 2

class ClsPath:
    trainPath        = f"./{PrivateSetting.datasetPath}/Train"
    validPath        = f"./{PrivateSetting.datasetPath}/Valid"
    testPath         = f"./{PrivateSetting.datasetPath}/Test"
    inferencePath    = f"./{PrivateSetting.datasetPath}/Inference"
    pretrainedWeight = f"./sample/PretrainedWeight/{SelectedModel.model['structure']}.pth"
    weightPath       = f"./{PrivateSetting.outputPath}/BestWeight.pth"