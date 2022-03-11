# -*- coding: utf-8 -*-

"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""

class PreprocessPara:
    ### normalize: 0: ImageNet, 1: CIFAR10, 2: MNIST, 3: Calculate normalize, 4: User Input, 5: ABF, 6: VRS
    normalize  = {'switch': False, 
                  'mode': 6,
                  'mean': [0.49002929, 0.49002929, 0.49002929],
                  'std': [0.26184613, 0.26184613, 0.26184613]}
    imageSize  = [224, 224] # resize the image before input to model
    # brightness = False
    # blur       = False
    # cutmix     = False
    # mosaic     = False