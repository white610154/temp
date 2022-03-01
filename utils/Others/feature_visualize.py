# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 09:25:51 2020

@author: LX
"""

#%%特徵視覺化
import matplotlib.pyplot as plt
import cv2
import torch
import numpy as np
from PIL import Image
import torch.nn as nn
from torchvision import models, transforms

from utils.ClsModel import resnext50_32x4d
from config.Config import ClsTest, ClsTrain

class SaveConvFeatures(): 
    
    def __init__(self, m): # module to hook
        self.hook = m.register_forward_hook(self.hook_fn) 
    def hook_fn(self, module, input, output): 
        self.features = output.data 
    def remove(self):
        self.hook.remove()

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
t = transforms.Compose([transforms.Resize((224, 224)), #128, 128
                        transforms.ToTensor(),
                        transforms.Normalize((0.49002929, 0.49002929, 0.49002929), (0.26184613, 0.26184613, 0.26184613))])

img_file = r'./input/Classification/Data/ten_type/test/EN01/2_3_630_6647_2_3_44.bmp'
img = Image.open(img_file)
img = img.convert(mode='RGB')
img = t(img).unsqueeze(0).to(device)

custom_model = resnext50_32x4d(pretrained=False)
num_ftrs = custom_model.fc.out_features
custom_model.Auofc = nn.Linear(num_ftrs, 10)
# print(custom_model.layer4)
# exit()

custom_model.load_state_dict(torch.load(ClsTest.weight_path))
custom_model = custom_model.to(device)
# custom_model.layer4是自己需要檢視特徵輸出的卷積層
hook_ref = SaveConvFeatures(custom_model.layer4)

with torch.no_grad():
    custom_model(img)
    
conv_features = hook_ref.features # [1,2048,7,7]
# print('dimension：', conv_features.shape)
hook_ref.remove()

def show_feature_map(img_src, conv_features):
    '''視覺化卷積層特徵圖輸出
    img_src:源影象檔案路徑
    conv_feature:得到的卷積輸出,[b, c, h, w]
    '''
    img = Image.open(img_src).convert('RGB')
    height, width = img.size
    heat = conv_features.squeeze(0)#降維操作,尺寸變為(2048,7,7)
    heat_mean = torch.mean(heat,dim=0)#對各卷積層(2048)求平均值,尺寸變為(7,7)
    heatmap = heat_mean.cpu().numpy()#轉換為numpy陣列
    heatmap /= np.max(heatmap)#minmax歸一化處理
    heatmap = cv2.resize(heatmap,(img.size[0],img.size[1]))#變換heatmap影象尺寸,使之與原圖匹配,方便後續視覺化
    heatmap = np.uint8(255*heatmap)#畫素值縮放至(0,255)之間,uint8型別,這也是前面需要做歸一化的原因,否則畫素值會溢位255(也就是8位顏色通道)
    heatmap = cv2.applyColorMap(heatmap,cv2.COLORMAP_JET)#顏色變換
    # plt.imshow(heatmap)
    # plt.show()
    # heatmap = np.array(Image.fromarray(heatmap).convert('L'))
    superimg = heatmap*0.4+np.array(img)[:,:,::-1] #影象疊加，注意翻轉通道，cv用的是bgr
    cv2.imwrite('./featureMap.jpg',superimg)#儲存結果
    # 視覺化疊加至源影象的結果
    # img_ = np.array(Image.open('./superimg.jpg').convert('RGB'))
    # plt.imshow(img_)
    # plt.show()


show_feature_map(img_file, conv_features)