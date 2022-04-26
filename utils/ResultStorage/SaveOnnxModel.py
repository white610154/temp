# -*- coding: utf-8 -*-

"""
Created on THU JAN 20 16:00:00 2022
@author: OtisChang
"""
import torch, os
from config.ConfigPreprocess import PreprocessPara
from config.Config import PrivateSetting
from config.ConfigPytorchModel import ClsModelPara

def onnx_pack(model, packageName, inputSize=PreprocessPara.resize["imageSize"], inputChannel=3):
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
    cudaDevice = torch.device('cuda:{}'.format(ClsModelPara.cudaDevice) if torch.cuda.is_available() else 'cpu')
    dummyInput = torch.randn(1, inputChannel, inputSize[0], inputSize[1]).cuda(cudaDevice)
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
