# -*- coding: utf-8 -*-

"""
Created on Jun Tue 14 22:00:00 2022
"""

def confidence_filter(resultList:list, classThresDict:dict) -> list:
    '''
        過濾指定類別, 並選擇信心分數高於門檻, 否則選擇次高的結果, 輸出最高分數的結果

        Args:
            resultList: 模型輸出結果
            'filename': 'BUMP_184_TOP_ok_70_31.bmp',
            'label': 'OK',
            'predict': 'OK',
            'confidence': 0.9999998807907104
            'output': {
                'NG': 8.45041796537771e-08,
                'OK': 0.9999998807907104
            }
            classThresDict: [分類類別: 信心分數門檻值]            
        Return:
            resultList: 過濾過的新輸出結果
    '''
    for result in resultList:
        (oriResultPredict, oriResultConfidence) = (result["predict"], result["confidence"])
        while result["predict"] in classThresDict.keys():
            if result["confidence"] >= classThresDict[result["predict"]]:
                break
            else:
                result["output"][result["predict"]] = 0
                resultClassOrder = sorted(result["output"].items(), key=lambda x:(x[1]), reverse=True)
                (result["predict"], result["confidence"]) = resultClassOrder[0]
                if result["confidence"] == 0:
                    (result["predict"], result["confidence"]) = (oriResultPredict, oriResultConfidence)
                    break
    return resultList