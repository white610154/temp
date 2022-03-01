import torch
import time
import copy
import numpy as np
from torch.utils.data import DataLoader
from .CustomDataset import ImageDataset, InferenceDataset
from .SelectTransform import select_train_transform, select_transform
from .SelectModel import select_model
from .SelectLossFunction import select_loss_function
from .SelectOptimizer import select_optimizer
from .SelectScheduler import select_scheduler
from utils.ResultStorage import DrawPlot, SaveAcc, SelectStorageMethod
from utils.Evaluation import ShowResult, SelectShowMethod
from utils.Postprocess.SetPostprocess import PostProcess
from config.ConfigPostprocess import PostProcessPara
from config.ConfigPytorchModel import ClsModelPara, ClsPath

### REPRODUCIBILITY
torch.manual_seed(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

def train():
    """
    Training procedure: 使用train的資料訓練模型，並紀錄訓練中的validation準確率並儲存權重

    Return:
        CheckPoint.pth、BestWeight.pth、FinalWeight.pth: 儲存記錄點、最佳權重及最終權重
        ValidAcc.txt: 紀錄valid的準確率變化
        ValidCurve.jpg: valid準確率變化曲線
    """
    ##### GPU setting #####
    cudaDevice = torch.device("cuda:{}".format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else "cpu")

    ##### Prepare data #####
    trainTransform = select_train_transform()
    trainSet = ImageDataset(ClsPath.trainPath, trainTransform)
    trainLoader = DataLoader(dataset=trainSet, batch_size=ClsModelPara.batchSize, shuffle=True, num_workers=0)
    print("Number of class : ", trainSet.numClasses)
    
    ##### Load model #####
    model = select_model()
    model = model.to(cudaDevice)
    model.train()

    ##### Define loss, optimizer, scheduler #####
    criterion = select_loss_function()
    optimizer = select_optimizer(model.parameters())
    scheduler = select_scheduler(optimizer)

    ##### Start training #####
    accRecord = []
    bestAcc = 0
    for epoch in range(ClsModelPara.epochs):
        localtime = time.asctime(time.localtime(time.time()))
        print('-' * len('Epoch: {}/{} --- < Starting Time : {} >'.format(epoch + 1, ClsModelPara.epochs,localtime)))
        print('Epoch: {}/{} --- < Starting Time : {} >'.format(epoch + 1, ClsModelPara.epochs, localtime))
        trainCorrect = 0

        for data in trainLoader:
            inputs, labels = data[0].to(cudaDevice), data[1].to(cudaDevice)
            optimizer.zero_grad()
            outputs = model(inputs)
            _, preds = torch.max(outputs.data, 1)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            trainCorrect += torch.sum(preds == labels)
        ShowResult.show_total_acc('Train', len(trainSet), trainCorrect)        
        validAcc = valid(cudaDevice, model, epoch)
        accRecord.append(validAcc)
        scheduler.step()

        ##### Save weight #####
        bestAcc = SelectStorageMethod.save_weight(model, bestAcc, validAcc, epoch)
    DrawPlot.draw_acc_curve(accRecord)


def valid(device, model, epoch:int):
    """
    Validation procedure: 使用valid的資料測試目前訓練階段的模型，得到準確率
    
    Args:
        device: 使用的GPU device
        model: 要驗證的模型
        epoch: 目前驗證的是第幾個epoch的模型

    Return:
        回傳valid的準確率
    """
    validTransform = select_transform()
    validSet = ImageDataset(ClsPath.validPath, validTransform)
    validLoader = DataLoader(dataset=validSet, batch_size=ClsModelPara.batchSize, shuffle=False, num_workers=0)

    classCorrect = [0.] * validSet.numClasses
    classTotal = [0.] * validSet.numClasses
    cfMatrix = np.zeros([len(validSet.className), len(validSet.className)])
    totalCorrect = 0
    total = 0
    modelClone = copy.deepcopy(model)
    modelClone.eval()
    with torch.no_grad():
        for data in validLoader:
            inputs, labels = data[0].to(device), data[1].to(device)
            outputs = modelClone(inputs)
            _, predicted = torch.max(outputs.data, 1)
            
            ##### Record the result #####
            total += labels.size(0)
            totalCorrect += (predicted == labels).sum().item()
            c = (predicted == labels)
            for i in range(labels.size(0)):
                classCorrect[labels[i]] += c[i].item()
                classTotal[labels[i]] += 1

        SaveAcc.save_epoch_acc(epoch, total, totalCorrect, classTotal, classCorrect, validSet.className)
    ##### Show predicted result #####
    SelectShowMethod.select_show_method('Valid', validSet, totalCorrect, classTotal, classCorrect, 
                                         cfMatrix, predicted, labels, confidence=None, count=None)
    return float(100 * totalCorrect / total)


def test():
    """
    Testing procedure: 使用test的資料測試指定權重之模型，並輸出結果csv和混淆矩陣

    Return:
        Test_result.csv: 輸出預測結果及信心值分布的csv檔
        ConfusionMatrix.jpg: 產生分類的混淆矩陣圖
    """
    cudaDevice = torch.device("cuda:{}".format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else "cpu")
    testTransform = select_transform()
    testSet = ImageDataset(ClsPath.testPath, testTransform)
    testLoader = DataLoader(dataset=testSet, batch_size=1, shuffle=False, num_workers=0)
    print("Number of class : ", testSet.numClasses)

    ##### Model define #####
    model = select_model()
    model.load_state_dict(torch.load(ClsPath.weightPath), strict=False)
    model = model.cuda(cudaDevice)
    model.eval()

    classCorrect = [0.] * len(testSet.className)
    classTotal = [0.] * len(testSet.className)
    totalCorrect = 0
    cfMatrix = np.zeros([len(testSet.className), len(testSet.className)])
    with torch.no_grad():
        count = 0
        countW = 0
        for data in testLoader:
            inputs, labels = data[0].to(cudaDevice), data[1].to(cudaDevice)
            outputs = model(inputs)
            
            ##### Post process #####
            testPostProcess = PostProcess(outputs, testSet.className)
            newOutputs = testPostProcess.select_process()
            _, predicted = torch.max(newOutputs, 1)
            
            ##### Record the result #####
            totalCorrect += (predicted == labels).sum().item()
            c = (predicted == labels)
            for i in range(labels.size(0)):
                classCorrect[labels[i]] += c[i].item()
                classTotal[labels[i]] += 1
                cfMatrix[int(labels[i]), int(predicted[i])] += 1

            ##### Output prediction csv #####
            confidence = torch.nn.functional.softmax(newOutputs, dim=1)
            count = SaveAcc.output_result_csv(testSet.filename, predicted, labels, confidence, testSet.className, count)
            countW = ShowResult.show_wrong_file(testSet.filename, predicted, labels, confidence, testSet.className, countW)

    ##### Show predicted result #####
    SelectShowMethod.select_show_method('Test', testSet, totalCorrect, classTotal, classCorrect, 
                                         cfMatrix, predicted, labels, confidence, count=None)
    DrawPlot.plot_confusion_matrix(cfMatrix, classes=testSet.className, normalize=True, title='Prediction result')


def inference():
    """
    Inference procedure: 使用訓練完成之模型辨識inference的資料，並輸出結果csv

    Return:
        Inference_result.csv: 輸出預測結果及信心值分布的csv檔
    """
    cudaDevice = torch.device("cuda:{}".format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else "cpu")
    inferenceTransform = select_transform()
    dataSet = InferenceDataset(ClsPath.inferencePath, inferenceTransform)
    dataLoader = DataLoader(dataset=dataSet, batch_size=1, shuffle=False, num_workers=0)

    ##### Load model #####
    model = select_model()
    model.load_state_dict(torch.load(ClsPath.weightPath), strict=False)
    model = model.cuda(cudaDevice)
    model.eval()

    className = PostProcessPara.confidenceFilter['classList']
    className.sort()
    className.sort(key=lambda x:x)
    with torch.no_grad():
        count = 0
        for data in dataLoader:
            inputs, labels = data[0].to(cudaDevice), data[1].to(cudaDevice)
            outputs = model(inputs)

            ##### Post process #####
            testPostProcess = PostProcess(outputs, className)
            newOutputs = testPostProcess.select_process()
            _, predicted = torch.max(newOutputs, 1)

            ##### Output result #####
            confidence = torch.nn.functional.softmax(outputs, dim=1)
            count = SaveAcc.output_result_csv(dataSet.filename, predicted, labels, confidence, className, count)