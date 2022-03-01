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
    # imgPath = os.path.join(PrivateSetting.DATASET_PATH, "Train")
    transform = transforms.Compose([transforms.Resize((imageSize[0], imageSize[1])), transforms.ToTensor()])
    trainDataset = ImageDataset(ClsPath.trainPath, transform=transform)
    dataloader = DataLoader(dataset=trainDataset, batch_size=32, shuffle=False)
    
    channels_sum, channels_squared_sum, num_batches = 0, 0, 0
    for data, _ in dataloader:
        # Mean over batch, height and width, but not over the channels
        channels_sum += torch.mean(data, dim=[0,2,3])
        channels_squared_sum += torch.mean(data**2, dim=[0,2,3])
        num_batches += 1
    
    mean = channels_sum / num_batches
    std = (channels_squared_sum / num_batches - mean ** 2) ** 0.5

    return mean, std