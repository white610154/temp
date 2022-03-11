# -*- coding: utf-8 -*-

"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""

import torch
from torch.utils.data import DataLoader
from torchvision import transforms

from config.ConfigPreprocess import *
from config.ConfigPytorchModel import ClsPath
from utils.ModelService.PytorchClassificationModel.CustomDataset import ImageDataset

def get_std_mean(imageSize):
    transform = transforms.Compose([transforms.Resize((imageSize[0], imageSize[1])), transforms.ToTensor()])
    trainDataset = ImageDataset(ClsPath.trainPath, transform=transform)
    dataloader = DataLoader(dataset=trainDataset, batch_size=1, shuffle=False)
    
    channelsSum, channelsSquaredSum, numBatches = 0, 0, 0
    for data, _ in dataloader:
        # Mean over batch, height and width, but not over the channels
        channelsSum += torch.mean(data, dim=[0, 2, 3])
        channelsSquaredSum += torch.mean(data ** 2, dim=[0, 2, 3])
        numBatches += 1
    
    mean = channelsSum / numBatches
    std = (channelsSquaredSum / numBatches - mean ** 2) ** 0.5
    return mean, std