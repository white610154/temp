import torch
import time
import copy
import numpy as np
from torch.utils.data import DataLoader
from .CustomDataset import ImageDataset, InferenceDataset
from .SelectTransform import select_train_transform, select_valid_transform, select_transform
from .SelectModel import select_model
from .SelectLossFunction import select_loss_function
from .SelectOptimizer import select_optimizer
from .SelectScheduler import select_scheduler
from utils.Postprocess.SetPostprocess import select_postprocess
from utils.ResultStorage import DrawPlot, SaveAcc, SelectStorageMethod, SaveUnknown
from utils.Evaluation import ShowResult, SelectShowMethod
from config.ConfigPostprocess import PostProcessPara
from config.ConfigPytorchModel import ClsModelPara, ClsPath
from config.Config import BasicSetting

### REPRODUCIBILITY
torch.manual_seed(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


def train():
    """
    Training procedure: Use training data for model training, and record epoch acc, best weight, and draw validation curve.

    Return:
        CheckPoint.pth、BestWeight.pth、FinalWeight.pth
        ValidAcc.txt: Record the validation accuracy of each epochs.
        ValidCurve.jpg: Draw the validation accuracy curve.
    """
    ##### GPU setting #####
    cudaDevice = torch.device('cuda:{}'.format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else 'cpu')

    ##### Prepare data #####
    trainTransform, normalization = select_train_transform()
    print("normalize in train: ", normalization)
    print("trainTransform: ", trainTransform)

    trainSet = ImageDataset(ClsPath.trainPath, trainTransform)
    trainLoader = DataLoader(dataset=trainSet, batch_size=ClsModelPara.batchSize, shuffle=True, num_workers=0)
    print('Number of class : ', trainSet.numClasses)

    ##### Load model #####
    model = select_model()
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
        print('-' * len('Epoch: {}/{} --- < Starting Time : {} >'.format(epoch + 1, ClsModelPara.epochs,localtime)))
        print('Epoch: {}/{} --- < Starting Time : {} >'.format(epoch + 1, ClsModelPara.epochs, localtime))
        trainCorrect = 0
        model.train()
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
        validAcc = valid(cudaDevice, model, epoch, normalization)
        accRecord.append(validAcc)
        scheduler.step()

        ##### Save weight #####
        bestAcc = SelectStorageMethod.save_weight(model, bestAcc, validAcc, epoch)
    DrawPlot.draw_acc_curve(accRecord)


def valid(device, model, epoch, normalization):
    """
    Validation procedure: Use validation data for model verification.

    Args:
        device: GPU device.
        model : The model used for verification.
        epoch : Current epoch of the model.

    Return:
        Record and return validation accuracy
    """
    print("========================= valid =========================")
    validTransform = select_valid_transform(normalization)
    # print("validTransform: ", validTransform)
    validSet = ImageDataset(ClsPath.validPath, validTransform)
    validLoader = DataLoader(dataset=validSet, batch_size=ClsModelPara.batchSize, shuffle=False, num_workers=0)

    classCorrect = [0.] * validSet.numClasses
    classTotal = [0.] * validSet.numClasses
    cfMatrix = np.zeros([len(validSet.className), len(validSet.className)])
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
        SelectStorageMethod.save_acc(epoch, total, totalCorrect, classTotal, classCorrect, validSet.className)
    ##### Show predicted result #####
    SelectShowMethod.select_show_method('Valid', validSet, totalCorrect, classTotal, classCorrect, cfMatrix)
    return float(100 * totalCorrect / total)


def test():
    """
    Testing procedure: Use test data for model verification, and output the predicted result csv and confusion matrix.

    Return:
        Test_result.csv: Record the filenames, labels, model prediction, and confidence.
        ConfusionMatrix.jpg: Confusion matrix graph.
    """
    cudaDevice = torch.device('cuda:{}'.format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else 'cpu')
    testTransform = select_transform()
    print("testTransform: ", testTransform)
    testSet = ImageDataset(ClsPath.testPath, testTransform)
    testLoader = DataLoader(dataset=testSet, batch_size=1, shuffle=False, num_workers=0)


    ##### Model define #####
    model = select_model()
    model.load_state_dict(torch.load(ClsPath.weightPath), strict=False)
    model = model.cuda(cudaDevice)
    model.eval()
    print('Number of class : ', testSet.numClasses)
    classCorrect = [0.] * testSet.numClasses
    classTotal = [0.] * testSet.numClasses
    totalCorrect = 0
    cfMatrix = np.zeros([testSet.numClasses, testSet.numClasses])
    with torch.no_grad():
        count, countW, countUnknown = 0, 0, 0

        for data in testLoader:
            inputs, labels = data[0].to(cudaDevice), data[1].to(cudaDevice)
            outputs = model(inputs)

            ##### Post process #####
            newOutputs = select_postprocess(outputs, testSet.className)
            _, predicted = torch.max(newOutputs, 1)

            ##### Record the result #####

            totalCorrect += (predicted == labels).sum().item()
            c = (predicted == labels)
            for i in range(labels.size(0)):
                classCorrect[labels[i]] += c[i].item()
                classTotal[labels[i]] += 1
                # cfMatrix[int(labels[i]), int(predicted[i])] += 1

            ##### Output prediction csv #####
            confidence = torch.nn.functional.softmax(newOutputs, dim=1)
            countUnknown = SaveUnknown.unknown_threshold(testSet.filename, predicted, labels, confidence, testSet.className, countUnknown)
            # count = SaveAcc.output_result_csv(testSet.filename, predicted, labels, confidence, testSet.className, count)
            countW = ShowResult.show_wrong_file(testSet.filename, predicted, labels, confidence, testSet.className, countW)

    ##### Show predicted result #####
    SelectShowMethod.select_show_method('Test', testSet, totalCorrect, classTotal, classCorrect, cfMatrix)
    SelectStorageMethod.test_acc(totalCorrect, classTotal, classCorrect)
    DrawPlot.plot_confusion_matrix(cfMatrix, classes=testSet.className, normalize=True, title='Prediction result')


def inference():
    """
    Inference procedure: Use trained model for classifying inference data, and output the result csv.

    Return:
        Inference_result.csv: Record the filenames, model prediction, and confidence.
    """
    cudaDevice = torch.device('cuda:{}'.format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else 'cpu')
    inferenceTransform = select_transform()
    print("inferenceTransform: ", inferenceTransform)
    dataSet = InferenceDataset(ClsPath.inferencePath, inferenceTransform)
    dataLoader = DataLoader(dataset=dataSet, batch_size=1, shuffle=False, num_workers=0)

    ##### Load model #####
    model = select_model()
    model.load_state_dict(torch.load(ClsPath.weightPath), strict=False)
    model = model.cuda(cudaDevice)
    model.eval()

    className = BasicSetting.classNameList
    className.sort()
    className.sort(key=lambda x:x)
    with torch.no_grad():
        count, countUnknown = 0, 0
        for data in dataLoader:
            inputs, labels = data[0].to(cudaDevice), data[1].to(cudaDevice)
            outputs = model(inputs)

            ##### Post process #####
            newOutputs = select_postprocess(outputs, className)
            score, predicted = torch.max(newOutputs, 1)

            ##### Output result #####
            confidence = torch.nn.functional.softmax(outputs, dim=1)

            countUnknown = SaveUnknown.unknown_threshold(dataSet.filename, predicted, labels, confidence, className, countUnknown)
            count = SaveAcc.output_result_csv(dataSet.filename, predicted, labels, confidence, className, count)