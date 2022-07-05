import os
import numpy as np
from PIL import Image
from torch.utils.data import Dataset

class ImageDataset(Dataset):
    """
    Custom Dataset of ImageDataset, which is used for train, valid and test
    """
    def __init__(self, rootDir, transform=None):
        self.rootDir = os.path.abspath(rootDir)
        self.x = []
        self.y = []
        self.imgSize = []
        self.filename = []
        self.transform = transform
        self.numClasses = 0
        self.className = os.listdir(self.rootDir)
        self.className.sort()
        self.className.sort(key=lambda x:x)
        for i, _dir in enumerate(self.className):
            fileList = os.listdir(os.path.join(self.rootDir, _dir))
            for j, file in enumerate(fileList):
                try:
                    image = Image.open(os.path.join(self.rootDir, _dir, file))
                    self.x.append(os.path.join(self.rootDir, _dir, file))
                    self.y.append(i)
                    self.filename.append(fileList[j])
                    self.imgSize = list(image.size)
                except:
                    continue
            self.numClasses += 1
    
    def __len__(self):
        return len(self.x)

    def __getitem__(self, index):
        image = Image.open(self.x[index]).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, self.y[index]



class InferenceDataset(Dataset):
    """
    Custom Dataset of ImageDataset, which is used for inference
    In this dataset, the label is all 0, cause inference data has no label.
    """
    def __init__(self, rootDir, transform=None):
        self.rootDir = rootDir
        self.x = []
        self.filename = []
        self.transform = transform
        for name in os.listdir(rootDir):
            try:
                Image.open(os.path.join(rootDir, name)).convert('RGB')
                self.filename.append(name)
                self.x.append(os.path.join(rootDir, name))
            except:
                continue
    
    def __len__(self):
        return len(self.filename)

    def __getitem__(self, index):
        image = Image.open(self.x[index]).convert('RGB')
        if self.transform:
            image = self.transform(image)
        # Inference has no label
        label = 0
        return image, label
