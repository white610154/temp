from config.Config import BasicSetting
from utils.ModelService.PytorchClassificationModel import MainProcess

def train():
    MainProcess.train()

def test():
    MainProcess.test()
    
def inference():
    MainProcess.inference()

def ai_model():
    print(f"========== Project: {BasicSetting.projectName}, Run:{BasicSetting.runId}, Mode:{BasicSetting.task} ==========")
    
    if BasicSetting.task == 'Train':
        train()
    elif BasicSetting.task == 'Test':
        test()
    elif BasicSetting.task == 'Inference':
        inference()
    else:
        raise BaseException("Please set up the correct task mode in config/Config.py.")

if __name__ == '__main__':
    
            
