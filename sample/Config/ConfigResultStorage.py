from config.Config import BasicSetting, PrivateSetting

class ResultStorage:
    saveFinalWeight     = {"switch": True}
    saveAccTxt          = {"switch": True}
    saveAccJson         = {"switch": True}
    savePredictResult   = {"switch": True}
    testAccJson         = {"switch": True}
    drawAccCurve        = {"switch": False}
    drawConfusionMatrix = {"switch": False}
    saveOnnxModel       = {"switch": True,  "fileName": BasicSetting.runId}
    saveCheckpoint      = {"switch": False, "saveIter": 1}
    unknownFilter       = {"switch": False,  "filter": {"unknown": 0.5}, "reverse": False, "saveCsv": 1}
