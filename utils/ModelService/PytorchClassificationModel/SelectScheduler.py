from config.ConfigModelService import SchedulerPara
import torch.optim.lr_scheduler as SchedulerMethod

def select_scheduler(optimizer):
    """
    According to configs in ConfigModelService, select scheduler to adjust learning rate of optimizer.

    Return:
        scheduler
    """
    if SchedulerPara.stepLR['switch']:
        method = getattr(SchedulerMethod, 'StepLR')
        scheduler = method(optimizer=optimizer, 
                           step_size=SchedulerPara.stepLR['stepSize'],
                           gamma=SchedulerPara.stepLR['gamma']
                           )
        
    elif SchedulerPara.cosineAnnealingLR['switch']:
        method = getattr(SchedulerMethod, 'CosineAnnealingLR')
        scheduler = method(optimizer=optimizer,
                           T_max=SchedulerPara.cosineAnnealingLR['tMax'],
                           eta_min=SchedulerPara.cosineAnnealingLR['etaMin'],
                           )
    return scheduler