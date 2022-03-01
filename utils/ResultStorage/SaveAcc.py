import os, csv
from torch import tensor
from config.Config import BasicSetting, PrivateSetting


def save_epoch_acc(epoch:int, total:int, totalCorrect:int, classTotal:list, classCorrect:list, className:list):
    """
    Save epoch accuracy into txt file.

    Args:
        epoch: 目前的epoch數
        total: 總資料量
        totalCorrect: 分類正確的總數
        classTotal: 各類別的資料總數
        classCorrect: 各類別分類正確的數量
        className: 類別名稱
    """
    if epoch == 0:
        with open(f'./{PrivateSetting.outputPath}/ValidAcc.txt','w') as fAcc:
            print('Validation acc of epoch {}: {:.4f} %'.format(epoch+1, 100 * totalCorrect / total), file = fAcc)
            for i, cls in enumerate(className):
                print('- Accuracy of class {:.5s} : {:.4f} %'.format(cls, 100 * classCorrect[i] / classTotal[i]), file = fAcc)
    else:
        with open(f'./{PrivateSetting.outputPath}/ValidAcc.txt','a') as fAcc:
            print('\nValidation acc of epoch {}: {:.4f} %'.format(epoch+1, 100 * totalCorrect / total), file = fAcc)
            for i, cls in enumerate(className):
                print('- Accuracy of class {:.5s} : {:.4f} %'.format(cls, 100 * classCorrect[i] / classTotal[i]), file = fAcc)


def output_result_csv(nameList:list, predict:tensor, labels:tensor, confidence:tensor, className:list, count:int, mode=BasicSetting.task):
    """
    Output 2 phase test result into csv file, file name : Data2_test_2phase_d23_c25.csv.

    Args:
        nameList: 所有檔案名稱列表
        predict: 預測類別結果
        labels: 原始輸入影像的正確類別
        confidence: 模型output經過softmax後的結果
        className: 所有的類別名稱
        count: 用來記錄目前的檔名到第幾個

    csv檔內的格式: 
        Filename | Ground truth | Prediction | Confidence of each class

    """
    ### Create csv file and title
    if mode == "Test":
        fileName = 'Test_result.csv'
        title = ['Filename', 'Ground truth', 'Prediction']
    elif mode =="Inference":
        fileName = 'Inference_result.csv'
        title = ['Filename', 'Prediction']
    if count == 0 :
        with open(os.path.join(PrivateSetting.outputPath, fileName), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            title.extend(className)
            writer.writerow(title)
            csvfile.close()

    ### Write result to csv file
    confidence = confidence.tolist()
    for i in range(len(predict)):
        fullname = nameList[count]
        with open(os.path.join(PrivateSetting.outputPath, fileName), 'a', newline='') as csvfile:
            if mode == "Test":
                result = [fullname, className[int(labels[i])], className[int(predict[i])]]
            elif mode == "Inference":
                result = [fullname, className[int(predict[i])]]
            result.extend(confidence[i][:10])
            writer = csv.writer(csvfile)
            writer.writerow(result)
        count += 1
    return count