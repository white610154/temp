from numpy import empty
from sklearn.covariance import empirical_covariance
import torch
from config.ConfigResultStorage import ResultStorage
from config.Config import BasicSetting, PrivateSetting
import os, csv
from torch import eq, tensor

def unknown_threshold(nameList, predict:tensor, labels:tensor, confidence:tensor, className, count:int, mode=BasicSetting.task):
    """
    Filter out images with scores below the threshold 

    Args:
        nameList: list include all file names
        predict: model prediction (dtype: tensor)
        labels: correct label (dtype:tensor)
        confidence: predicted confidence
        className: class name of each class  
        count: use to record current file
    """
    if ResultStorage.unknownFilter["switch"]:
        filterDict = ResultStorage.unknownFilter["filter"]
        filter = sorted(filterDict.items(), key=lambda x:x[1], reverse=ResultStorage.unknownFilter["reverse"]) # x[1]: score
        fileName = f'Test_filter.csv' if mode == "Test" else f'Inference_filter.csv'
        title = ['Filename', 'Ground truth', 'type', 'sorce']
        
        if count == 0 and ResultStorage.unknownFilter["saveCsv"]:
            with open(os.path.join(PrivateSetting.outputPath, fileName), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(title)  
                csvfile.close()

        confid = confidence.cpu().numpy()
        for i in range(len(predict)):
            score = confid[i, predict[i]]
            fullname = nameList[count]
            result = []
            for tagName, threshold in filter:
                if score < threshold and not ResultStorage.unknownFilter["reverse"]:
                    print(f'{tagName} file: {fullname}, Label: {className[int(labels[i])]}, sorce({score:.2f}) < threshold({threshold})')
                    result = [fullname, className[int(labels[i])], tagName, f'{score:.2f}']
                    break    
                elif score > threshold and ResultStorage.unknownFilter["reverse"]:
                    print(f'{tagName} file: {fullname}, Label: {className[int(labels[i])]}, sorce({score:.2f}) > threshold({threshold})')
                    result = [fullname, className[int(labels[i])], tagName, f'{score:.2f}']
                    break
            if ResultStorage.unknownFilter["saveCsv"] and len(result) != 0:
                with open(os.path.join(PrivateSetting.outputPath, fileName), 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(result)
            count += 1
    return count
    
