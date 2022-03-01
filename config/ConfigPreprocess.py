# -*- coding: utf-8 -*-

"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""

### 資料前處理 ###

class PreprocessPara:
    imageSize  = [224, 224]
    normalize  = {'switch': True, 
                  'mode': 4,  # 0: ImageNet, 1: CIFAR10, 2: MNIST, 3: Calculate normalize, 4: User Input 
                  'mean': (0.49002929, 0.49002929, 0.49002929),
                  'std': (0.26184613, 0.26184613, 0.26184613)}
    brightness = False
    blur       = False
    cutmix     = False
    mosaic     = False