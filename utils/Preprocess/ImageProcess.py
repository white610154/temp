# -*- coding: utf-8 -*-

"""
Created on MON Mar 7 11:00:00 2022
@author: OtisChang
"""
from PIL import ImageEnhance, Image

def bright_enhance(image, brightness=0.8):
    enhBri = ImageEnhance.Brightness(image)
    newImg = enhBri.enhance(brightness)

    return newImg

def contrast_enhance(image, contrast = 2):
    newImg = ImageEnhance.Contrast(image).enhance(contrast)  
    return newImg

def color_sharp(image, factor=2):
    enh_sha = ImageEnhance.Sharpness(image)
    newImg = enh_sha.enhance(factor=1.5)
    return newImg

def rotate(image, angle=90):
    if angle == 90:
        newImg = image.transpose(Image.ROTATE_90)
    if angle == 180:
        newImg = image.transpose(Image.ROTATE_180)
    if angle == 270:
        newImg = image.transpose(Image.ROTATE_270)
    return newImg
