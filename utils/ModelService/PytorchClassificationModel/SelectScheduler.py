from torch import optim
from config.ConfigModelService import SchedulerPara
import torch.optim.lr_scheduler as SchedulerMethod

def select_scheduler(optimizer):
    if SchedulerPara.stepLR['switch']:
        method = getattr(SchedulerMethod, 'StepLR')
        scheduler = method(optimizer=optimizer, 
                           step_size=SchedulerPara.stepLR['step_size'],
                           gamma=SchedulerPara.stepLR['gamma']
                           )
        
    elif SchedulerPara.cosineAnnealingLR['switch']:
        method = getattr(SchedulerMethod, 'CosineAnnealingLR')
        scheduler = method(optimizer=optimizer,
                           T_max=SchedulerPara.cosineAnnealingLR['T_max'],
                           eta_min=SchedulerPara.cosineAnnealingLR['eta_min'],
                           )
    
    return scheduler