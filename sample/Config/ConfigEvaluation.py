class EvaluationPara:
    accuracy = {"switch": True, "mode": ['Train', 'Valid', 'Test'], "saveTxt": True, "saveJson": True}
    accOfClasses = {"switch": True, "mode": ['Valid', 'Test'], "saveTxt": True, "saveJson": True}
    numOfClasses = {"switch": True, "mode": ['Valid', 'Test'], "saveTxt": True, "saveJson": True}
    otherClsRate = {"switch": False, "posClass": [], "negClass": [], "saveTxt" : True, "saveJson": True}
    drawAccCurve = {"switch": True} 
    drawConfusionMatrix = {"switch": True, "showNumber": True}