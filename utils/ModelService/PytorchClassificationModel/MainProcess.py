import torch
import time, os
import numpy as np
from torch.utils.data import DataLoader
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from config.Config import BasicSetting
from config.ConfigPytorchModel import ClsModelPara, ClsPath, SelectedModel
from config.ConfigPreprocess import PreprocessPara
from .CustomDataset import ImageDataset, InferenceDataset
from .SelectTransform import select_train_transform, select_valid_transform, select_transform
from .SelectModel import select_model
from .SelectLossFunction import select_loss_function
from .SelectOptimizer import select_optimizer
from .SelectScheduler import select_scheduler
from utils.Preprocess.SelectNormalization import set_normalize
from utils.Evaluation import SelectEvaluationMethod
from utils.ResultStorage import SelectStorageMethod

### REPRODUCIBILITY
torch.manual_seed(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

def train() -> None:
    """
    Training procedure: Use training data for model training, and record epoch acc, best weight, and draw validation curve.

    Return:
        weight.pth and weight.onnx: for saving weight
        TrainAcc.json, TrainAcc.txt, ValidAcc.json, ValidAcc.txt and ValidAcc.jpg: for saving training record
    """
    ##### Define GPU #####
    cudaDevice = torch.device('cuda:{}'.format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else 'cpu')

    ##### Prepare data #####
    normalizedValue = set_normalize(PreprocessPara, 'train')
    trainTransform = select_train_transform(normalizedValue)
    trainSet = ImageDataset(ClsPath.trainPath, trainTransform)
    trainLoader = DataLoader(dataset=trainSet, batch_size=ClsModelPara.batchSize, shuffle=True, num_workers=0)
    print('Number of class : ', trainSet.numClasses)

    ##### Load model #####
    if PreprocessPara.resize["switch"]:
        imgSize = PreprocessPara.resize["imageSize"]
    else:
        imgSize = trainSet.imgSize
    model = select_model(imgSize)
    model = model.to(cudaDevice)

    ##### Define loss, optimizer, scheduler #####
    criterion = select_loss_function()
    optimizer = select_optimizer(model.parameters())
    scheduler = select_scheduler(optimizer)

    ##### Start training #####
    accRecord = []
    bestAcc = 0
    for epoch in range(ClsModelPara.epochs):
        localtime = time.asctime(time.localtime(time.time()))
        lineLength = len('Epoch: {}/{} --- < Starting Time : {} >'.format(epoch + 1, ClsModelPara.epochs,localtime))
        singleLine = '-' * (int(lineLength/2) - 3)
        print('=' * lineLength)
        print(singleLine + ' train ' + singleLine)
        print('Epoch: {}/{} --- < Starting Time : {} >'.format(epoch + 1, ClsModelPara.epochs, localtime))
        trainCorrect = 0
        model.train()
        for data in trainLoader:
            inputs, labels = data[0].to(cudaDevice), data[1].to(cudaDevice)
            optimizer.zero_grad()
            try:
                outputs = model(inputs)
            except:
                raise ValueError(f'Please set resize["switch"]: True and resize["imageSize"]: [224, 244] in config/ConfigPreprocess to make sure that model can be trained correctly.')
            _, preds = torch.max(outputs.data, 1)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            trainCorrect += torch.sum(preds == labels)
        
        ##### Save training evaluation #####
        SelectEvaluationMethod.select_train_evaluation(totalNumbers=len(trainSet), totalCorrect=trainCorrect,
                                                       totalEpoch=ClsModelPara.epochs, epoch=epoch)
        
        ##### Validation #####
        print(singleLine + ' valid ' + singleLine)
        validAcc = valid(cudaDevice, model, epoch, normalizedValue)
        
        ##### Record for drawing curve #####
        accRecord.append(validAcc)
        
        ##### Modify learning rate #####
        scheduler.step()
        
        ##### Save weight #####
        bestAcc = SelectStorageMethod.save_model(SelectedModel.model["structure"], model, optimizer, cudaDevice, bestAcc, validAcc, epoch)
    
    ##### Draw Curve #####
    SelectEvaluationMethod.select_valid_plot(accRecord)

def valid(device, model, epoch, normalizedValue) -> float:
    """
    Validation procedure: Use validation data for model verification.

    Args:
        device: GPU device.
        model : The model used for verification.
        epoch : Current epoch of the model.
    Return:
        Return validation accuracy
        ValidAcc.json, ValidAcc.txt and ValidAcc.jpg: for saving training record
    """
    validTransform = select_valid_transform(normalizedValue)
    validSet = ImageDataset(ClsPath.validPath, validTransform)
    validLoader = DataLoader(dataset=validSet, batch_size=ClsModelPara.batchSize, shuffle=False, num_workers=0)

    classCorrect = [0.] * validSet.numClasses
    classTotal = [0.] * validSet.numClasses
    totalCorrect = 0
    total = 0
    model.eval()
    with torch.no_grad():
        for data in validLoader:
            inputs, labels = data[0].to(device), data[1].to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            
            ##### Record the result #####
            total += labels.size(0)
            totalCorrect += (predicted == labels).sum().item()
            c = (predicted == labels)
            for i in range(labels.size(0)):
                classCorrect[labels[i]] += c[i].item()
                classTotal[labels[i]] += 1
    
    ##### Save validation record #####
    SelectEvaluationMethod.select_evaluation(task='Valid', totalNumbers=len(validSet), totalCorrect=totalCorrect,
                                             perClassNumbers=classTotal, perClassCorrect=classCorrect, className=validSet.className,
                                             totalEpoch=ClsModelPara.epochs, epoch=epoch)
    if total == 0:
        return 0
    else:
        return float(100 * totalCorrect / total)

def test() -> list:
    """
    Testing procedure: Use test data for model verification, and output the predicted result csv and confusion matrix.

    Return:
        resultList: model predicts result
        perResultDict = {
            "filename": filename,
            "label": label className,
            "predict": predict className,
            "confidence": confidence score,
            "output": confDict - confidence from all classes
        }
    """
    ##### Define GPU #####
    cudaDevice = torch.device('cuda:{}'.format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else 'cpu')
    normalizedValue = set_normalize(PreprocessPara, 'test')
    testTransform = select_transform(normalizedValue)
    testSet = ImageDataset(ClsPath.testPath, testTransform)
    testLoader = DataLoader(dataset=testSet, batch_size=1, shuffle=False, num_workers=0)

    ##### Model define #####
    model = select_model()
    model = model.to(cudaDevice)
    model.eval()
    print('Number of class : ', testSet.numClasses)
    resultList = []
    with torch.no_grad():
        for filenameCount, data in enumerate(testLoader):
            inputs, labels = data[0].to(cudaDevice), data[1].to(cudaDevice)
            try:
                outputs = model(inputs)
            except:
                raise ValueError(f'Please correctly set resize in config/ConfigPreprocess to make sure that model can work correctly.')
            outputs = outputs[0][:testSet.numClasses]
            outputs = outputs[None, :]
            _, predicted = torch.max(outputs, 1)
            confidence = torch.nn.functional.softmax(outputs, dim=1)

            ##### record each score for each class #####
            confDict = {}
            for classNameCount, conf in enumerate(confidence[0]):
                confDict[testSet.className[classNameCount]] = float(conf)
            
            ##### record each result #####
            perResultDict = {
                "filename": testSet.filename[filenameCount],
                "label": testSet.className[labels[0]],
                "predict": testSet.className[predicted[0]],
                "confidence": float(confidence[0][predicted[0]]),
                "output": confDict
            }

            resultList.append(perResultDict)
    return resultList

def inference() -> list:
    """
    Inference procedure: Use trained model for classifying inference data, and output the result csv.

    Return:
        resultList: model predicts result
        perResultDict = {
            "filename": filename,
            "label": label className,
            "predict": predict className,
            "confidence": confidence score,
            "output": confDict - confidence from all classes
        }
    """
    ##### Define GPU #####
    cudaDevice = torch.device('cuda:{}'.format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else 'cpu')
    normalizedValue = set_normalize(PreprocessPara, 'test')
    inferenceTransform = select_transform(normalizedValue)
    dataSet = InferenceDataset(ClsPath.inferencePath, inferenceTransform)
    dataLoader = DataLoader(dataset=dataSet, batch_size=1, shuffle=False, num_workers=0)

    ##### Load model #####
    model = select_model()
    model = model.to(cudaDevice)
    model.eval()

    ##### Set class #####
    className = BasicSetting.classNameList
    className.sort()
    className.sort(key=lambda x:x)
    print('Number of class : ', len(className))
    resultList = []
    with torch.no_grad():
        for filenameCount, data in enumerate(dataLoader):
            inputs, labels = data[0].to(cudaDevice), data[1].to(cudaDevice)
            try:
                outputs = model(inputs)
            except:
                raise ValueError(f'Please correctly set resize in config/ConfigPreprocess to make sure that model can work correctly.')
            outputs = outputs[0][:len(className)]
            outputs = outputs[None, :]
            _, predicted = torch.max(outputs, 1)
            confidence = torch.nn.functional.softmax(outputs, dim=1)

            ##### record each score for each class #####
            confDict = {}
            for classNameCount, conf in enumerate(confidence[0]):
                confDict[className[classNameCount]] = float(conf)
            
            ##### record each result #####
            perResultDict = {
                "filename": dataSet.filename[filenameCount],
                "predict": className[predicted[0]],
                "label": None,
                "confidence": float(confidence[0][predicted[0]]),
                "output": confDict
            }

            resultList.append(perResultDict)
    return resultList