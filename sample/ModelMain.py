from config.Config import BasicSetting
from utils.ModelService.PytorchClassificationModel import MainProcess

def train():
    MainProcess.train()

def test():
    MainProcess.test()
    
def inference():
    MainProcess.inference()

def model_main():
    print(f"========== Project: {BasicSetting.projectName}, Run:{BasicSetting.runId}, Mode:{BasicSetting.task} ==========")
    try:
        if BasicSetting.task == 'Train':
            train()
        elif BasicSetting.task == 'Test':
            test()
        elif BasicSetting.task == 'Inference':
            inference()
        else:
            raise BaseException("Please set up the correct task mode in config/Config.py.")
        return True
    except Exception as err:
        print(err)
        return False

if __name__ == "__main__":
    model_main()