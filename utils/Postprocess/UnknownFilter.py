# -*- coding: utf-8 -*-

"""
Created on Jun Tue 14 22:00:00 2022
"""

def unknown_filter(resultList:list, classThresDict:dict, reverse:bool=False) -> list:
    '''
        過濾指定類別, 判成新類別

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
            reverse: 升冪或降冪   
        Return:
            resultList: 過濾過的新輸出結果
    '''
    filterClassOrder = sorted(classThresDict.items(), key=lambda x:(x[1]), reverse=(not reverse))
    for result in resultList:
        for filterClass in filterClassOrder:
            if (not reverse and result["confidence"] < filterClass[1]) or (reverse and result["confidence"] > filterClass[1]):
                (result["predict"], result["confidence"]) = filterClass
    return resultList