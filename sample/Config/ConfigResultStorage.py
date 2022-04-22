class ResultStorage:
    saveFinalWeight     = {"switch": True}
    saveAccTxt          = {"switch": True}
    saveAccJson         = {"switch": True}
    drawAccCurve        = {"switch": False}
    drawConfusionMatrix = {"switch": False}
    saveOnnxModel       = {"switch": False,  "fileName": 'onnxModel'}
    saveCheckpoint      = {"switch": False, "saveIter": 1}
    unknownFilter       = {"switch": False,  "filter"  : {"unknown" : 0.5}, "reverse" : False, "saveCsv" : True}
