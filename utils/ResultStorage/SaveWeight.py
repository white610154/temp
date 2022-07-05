import os, torch
from config.Config import PrivateSetting
from config.ConfigPreprocess import PreprocessPara
 ### 阿阿阿世亞對不起這邊都還給你啦

def create_folder(folderPath=PrivateSetting.outputPath):
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath)


def save_weight(model, weightName):
    """
    Save the Model parameters in DictPth.

    Args:
        model: the entire model
        weightName: the saved weight file name
    Output:
        xxx.pth: the weight file of model
    """
    create_folder()
    torch.save(model.state_dict(), f'{PrivateSetting.outputPath}/{weightName}.pth')


def save_model_optimizer(epoch, model, optimizer, weightName):
    """
    Save epoch, model and optimizer parameters for avoiding unexpected interruption.

    Args:
        epoch: current epoch number
        model: the entire model
        optimizer: the entire optimizer
        weightName: the saved weight file name
    Output:
        checkpoint.pth: include "epoch", "model", "optimizer" parameters
    """
    create_folder()  
    torch.save({
                "epoch": epoch,
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict()
                }, f'{PrivateSetting.outputPath}/{weightName}.pth')


def save_script_model(model, weightName='FinetuneModel'):
    """
    Save the whole Model in ScriptPth which include parameters and structure.

    Args:
        model: the entire model
        weightName: the saved weight file name
    Output:
        FinetuneModel.pth: pth file with TorchScript model
    """
    create_folder()
    model_scripted = torch.jit.script(model)
    model_scripted.save(f'{PrivateSetting.outputPath}/{weightName}.pth')


def onnx_pack(model, cudaDevice, packageName, inputSize=PreprocessPara.resize["imageSize"], inputChannel=3):
    """
    Pack pytorch model into onnx model under the cuda state and save onnx file.

    Args:
        model: whole pytorch model including structure and weighted parameter
        packageName: saved onnx model name
        inputSize (list): image size that input to model
        inputChannel: number of image channel
    Return:
        .onnx file: onnx model file
    """
    model.eval()
    
    dummyInput = torch.randn(1, inputChannel, inputSize[0], inputSize[1]).to(cudaDevice)
    packagePath = os.path.join(PrivateSetting.outputPath, f'{packageName}.onnx')
    inputNames = ["input"]
    outputNames = ["output"]

    torch.onnx.export(
        model,                    # 要打包的模型
        dummyInput,               # 模型輸入大小
        packagePath,              # 輸出的打包檔名稱
        input_names=inputNames,   # 輸入層的名稱，驗證時要對應相同的input_names
        output_names=outputNames, # 輸出層的名稱
        export_params=True,       # 連參數權重一併打包輸出
    )
