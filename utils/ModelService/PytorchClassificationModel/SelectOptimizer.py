import torch
import torch.optim as OptimizerMethod
from config.ConfigModelService import OptimizerPara, LearningRate

def select_optimizer(modelPara):
    if OptimizerPara.SGD['switch']:
        method = getattr(OptimizerMethod, 'SGD')
        optimizer = method(params=modelPara, 
                           lr=LearningRate.learningRate,
                           momentum=OptimizerPara.SGD['momentum'],
                           dampening=OptimizerPara.SGD['dampening'],
                           weight_decay=OptimizerPara.SGD['weightDecay'],
                           nesterov=OptimizerPara.SGD['nesterov'],
                           )
        
    elif OptimizerPara.Adam['switch']:
        method = getattr(OptimizerMethod, 'Adam')
        optimizer = method(params=modelPara, 
                           lr=LearningRate.learningRate,
                           betas=OptimizerPara.Adam['betas'],
                           eps=OptimizerPara.Adam['eps'],
                           weight_decay=OptimizerPara.Adam['weightDecay'],
                           amsgrad=OptimizerPara.Adam['amsgrad'],
                           )

    elif OptimizerPara.Adadelta['switch']:
        method = getattr(OptimizerMethod, 'Adadelta')
        optimizer = method(params=modelPara, 
                           lr=LearningRate.learningRate,
                           rho=OptimizerPara.Adadelta['rho'],
                           eps=OptimizerPara.Adadelta['eps'],
                           weight_decay=OptimizerPara.Adadelta['weightDecay'],
                           )
    
    elif OptimizerPara.AdamW['switch']:
        method = getattr(OptimizerMethod, 'AdamW')
        optimizer = method(params=modelPara, 
                           lr=LearningRate.learningRate,
                           betas=OptimizerPara.AdamW['betas'],
                           eps=OptimizerPara.AdamW['eps'],
                           weight_decay=OptimizerPara.AdamW['weightDecay'],
                           amsgrad=OptimizerPara.AdamW['amsgrad'],
                           )
    
    elif OptimizerPara.NAdam['switch']:
        if torch.__version__ > '1.10.0':
            raise BaseException(f"NAdam needs torch version >= 1.10.0. But the torch version is {torch.__version__}.")
        else:
            method = getattr(OptimizerMethod, 'NAdam')
            optimizer = method(params=modelPara, 
                            lr=LearningRate.learningRate,
                            betas=OptimizerPara.NAdam['betas'],
                            eps=OptimizerPara.NAdam['eps'],
                            weight_decay=OptimizerPara.NAdam['weightDecay'],
                            momentum_decay=OptimizerPara.NAdam['momentumDecay'],
                            amsgrad=OptimizerPara.NAdam['amsgrad'],
                            )
    
    return optimizer