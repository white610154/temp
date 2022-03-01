# -*- coding: utf-8 -*-

"""
Created on Wed Jan 12 14:00:00 2022
@author: OtisChang
"""

import cv2, os
from config.Config import datasetPath

def main(coor):
    imagePath = datasetPath + '/Image/'
    fileList = os.listdir(imagePath)
    for fileLine in fileList:
        if fileLine.split('.')[-1] == 'bmp' or fileLine.split('.')[-1] == 'jpg':
            image = cv2.imread(imagePath + fileLine)
            resizeImage = cv2.resize(image, (coor[0], coor[1]), interpolation=cv2.INTER_AREA)
            cv2.imwrite(imagePath + fileLine, resizeImage)
