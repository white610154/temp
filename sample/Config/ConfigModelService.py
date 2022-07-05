from config.ConfigPytorchModel import ClsModelPara

class LossFunctionPara:
    lossFunction = 'CrossEntropyLoss'

class LearningRate:
    learningRate = 0.001

class OptimizerPara:
    SGD = {"switch": False, "momentum": 0.9, "dampening": 0, "weightDecay": 5e-4, "nesterov": False}
    Adam = {"switch": False, "betas": [0.9, 0.999], "eps": 1e-8, "weightDecay": 0, "amsgrad": False}
    Adadelta = {"switch": False, "rho": 0.9, "eps": 1e-6, "weightDecay": 0}
    AdamW = {"switch": False, "betas": [0.9, 0.999], "eps": 1e-8, "weightDecay": 0.01, "amsgrad": False}
    NAdam = {"switch": False, "betas": [0.9, 0.999], "eps": 1e-8, "weightDecay": 0, "momentumDecay": 0.004}

class SchedulerPara:
    stepLR = {"switch": False, "stepSize": 1, "gamma": 0.1}
    cosineAnnealingLR = {"switch": False, "tMax": 1, "etaMin": 0}



   
