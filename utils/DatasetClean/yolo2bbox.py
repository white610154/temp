import os
import math

from PIL import Image

def round_operation(number):
    '''
    對數字進行四捨五入的操作
    '''
    if math.ceil(number) - number > 0.5:
        num = math.floor(number)
    else:
        num = math.ceil(number)

    return num


def yolo_to_bbox(yoloPath, outputPath, imgPath):
    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)
    for txtfile in os.listdir(yoloPath):
        im = Image.open(os.path.join(imgPath, txtfile[:-4] + '.bmp'))
        Width, Height = im.size

        with open(os.path.join(outputPath, txtfile), 'a') as outputf:
            with open(os.path.join(yoloPath, txtfile), 'r') as inputf:
                labelList = inputf.readlines()
                for label in labelList:
                    label = label.split(' ')
                    clsType = label[0]
                    x = float(label[1])
                    y = float(label[2])
                    w = float(label[3])
                    h = float(label[4])
                    
                    xmin = (x - w / 2) * Width
                    ymin = (y - h / 2) * Height
                    xmax = (x + w / 2) * Width
                    ymax = (y + h / 2) * Height
                    print(xmin, ymin, xmax, ymax)
                    print('{} {} {} {} {}'.format(clsType, round_operation(xmin), round_operation(ymin), round_operation(xmax), round_operation(ymax)), file=outputf)



if __name__ == '__main__':
    yoloPath = './2048_Yolo'
    imgPath = './0923'
    outputPath = './Txt_BBox'

    yolo_to_bbox(yoloPath, outputPath, imgPath)