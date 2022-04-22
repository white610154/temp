import shutil
import os, cv2, csv
import numpy as np
import xml.etree.ElementTree as ET
from PIL import Image


def dataset_divide(TXT_PATH:str, RAW_DATA_PATH:str, OUTPUT_PATH:str, Dataset:list):
    """
    依照TXT_PATH下Test_0923_test, Test_0923_train, Test_0923_valid三個txt檔中的檔名列表切分檔案到三個資料夾下

    Args:
        TXT_PATH: txt檔的路徑，下含三個txt檔
        RAW_DATA_PATH: 原始所有影像的路徑
        OUTPUT_PATH: 輸出切分結果的路徑
        Dataset: 要切分的資料集種類，與txt檔數量相同

    Return:
        dataset_path: 各資料集資料夾的路徑，下含要切defect的原始圖片
    """
    print("Dataset dividing ...")

    dataset_path = []
    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    for i in range(len(Dataset)):
        if not os.path.isdir(os.path.join(OUTPUT_PATH, Dataset[i])):
            os.mkdir(os.path.join(OUTPUT_PATH, Dataset[i]))
        dataset_path.append(os.path.join(OUTPUT_PATH, Dataset[i]))

    for i in range(len(Dataset)):
        txtfile = os.path.join(TXT_PATH, 'Test_0923_' + Dataset[i] + '.txt')

        f = open(txtfile, 'r')
        for line in f.readlines():
            shutil.copy(os.path.join(RAW_DATA_PATH, line[:-1]), 
                    os.path.join(OUTPUT_PATH, Dataset[i], line[:-1]))
    
    return dataset_path



def crop_defect_fromtxt(ANNOTATION_PATH:str, dataset_path:str, OUTPUT_PATH:str, Dataset:list, className:list):
    """
    將資料夾下的原始圖片依據txt所記錄的Bbox座標切出defect，並存到OUTPUT_PATH的crop資料夾中
    defect圖的檔名格式為 桿頭編號-面向_xmin_ymin_xmax_ymax_類別(eg. 20210923134554SM-A_D171_9_TOTAL_V0-CROWN1_337_449_348_458_A)

    Args:
        ANNOTATION_PATH: annotation檔的路徑，路徑下為所有的txt檔，檔名與圖片的檔名對應
        dataset_path: 要切出defect的目標資料夾，下含要切defect的原始圖片
        OUTPUT_PATH: 輸出切分結果的路徑，切好defect的圖會存在其下的crop資料夾
        Dataset: 要切分的資料集種類，與txt檔數量相同
        className: 要切分的defect種類

    Return:
        cropSetPath: 要切分類別資料夾的路徑，其下包含defect圖
    """
    print("Cropping defect according to txt file ...")

    cropSetPath = []
    for i, name in enumerate(Dataset):
        resultFolder = os.path.join(OUTPUT_PATH, 'crop_' + name)
        cropSetPath.append(resultFolder)
        if not os.path.isdir(resultFolder):
            os.mkdir(resultFolder)

        fileList = os.listdir(dataset_path[i])

        total_class = 0
        total_data = 0
        for fileName in fileList:
            # print(fileName)
            f = open(ANNOTATION_PATH + fileName[:-4] + '.txt', 'r')
            img = cv2.imread(os.path.join(dataset_path[i], fileName))


            for line in f.readlines():
                total_data += 1
                if int(line[0]) > total_class:
                    total_class = int(line[0])
                class_num = int(line.split(' ')[0])
                xmin = int(line.split(' ')[1])
                ymin = int(line.split(' ')[2])
                xmax = int(line.split(' ')[3])
                ymax = int(line.split(' ')[4])

                # print(ymin, ymax, xmin, xmax)
                cropImg = img[ymin : ymax, xmin : xmax]
                cv2.imwrite(os.path.join(resultFolder, fileName[:-4] + '_' + str(xmin) + '_' + str(ymin) + '_' + str(xmax) + '_' + str(ymax) + '_' + className[class_num] + '.jpg'), cropImg)

                ############ Paste to black background ############
                # blank_image = np.zeros((768, 768, 3), np.uint8)
                # result_image = Image.fromarray(blank_image)
                # cropImg = Image.fromarray(cv2.cvtColor(cropImg, cv2.COLOR_BGR2RGB))
                # x_shift = round((int(xmax) - int(xmin)) / 2)
                # y_shift = round((int(ymax) - int(ymin)) / 2)
                # result_image.paste(cropImg, (384 - x_shift, 384 - y_shift))
                # result_image.save(outputPath + fileName[:-4] + '_' + str(xmin) + '_' + 
                #                   str(ymin) + '_' + str(xmax) + '_' + str(ymax) + '_' + className[class_num] + '.jpg')
                ############ Paste to black background ############
        print("- {} set has {} classes, total data : {}".format(name, total_class + 1, total_data))
    
    return cropSetPath


def crop_defect_fromxml(xml_path:str, OUTPUT_PATH:str, Dataset:list):
    """
    將資料夾下的原始圖片依據xml所記錄的Bbox座標切出defect，並存到OUTPUT_PATH的crop資料夾中
    defect圖的檔名格式為 桿頭編號-面向_xmin_ymin_xmax_ymax_類別(eg. 20210923134554SM-A_D171_9_TOTAL_V0-CROWN1_337_449_348_458_A)

    Args:
        xml_path: annotation檔的路徑，路徑下為所有的xml檔，檔名與圖片的檔名對應
        OUTPUT_PATH: 輸出切分結果的路徑，切好defect的圖會存在其下的crop資料夾
        Dataset: 要切分的資料集種類，與txt檔數量相同
        
    Returm:
        cropSetPath: 要切分類別資料夾的路徑，其下包含defect圖
    """
    print("Cropping defect according to xml file ...")

    cropSetPath = []
    for name in Dataset:
        resultFolder = os.path.join(OUTPUT_PATH, 'crop_' + name)
        cropSetPath.append(resultFolder)

        if not os.path.isdir(resultFolder):
            os.mkdir(resultFolder)

        folder = os.path.join(OUTPUT_PATH, name)
        fileList = os.listdir(folder)

        for fileName in fileList:
            img = cv2.imread(os.path.join(folder, fileName))
            tree = ET.parse(xml_path + fileName[:-4] + '.xml')
            root = tree.getroot()        
            for obj in root.findall('object'):
                name = obj.find('name').text
                bndBox = obj.find('bndBox')
                xmin = bndBox.find('xmin').text
                ymin = bndBox.find('ymin').text
                xmax = bndBox.find('xmax').text
                ymax = bndBox.find('ymax').text

                # print(fileName, type(name))
                # print(int(ymin), int(ymax), int(xmin), int(xmax))
                cropImg = img[int(ymin) : int(ymax), int(xmin) : int(xmax)]
                cv2.imwrite(os.path.join(resultFolder, fileName[:-4] + '_' + str(xmin) + '_' + str(ymin) + '_' + str(xmax) + '_' + str(ymax) + '_' + name + '.jpg'), cropImg)
    return cropSetPath


def classfolder_divide(cropSetPath:str):
    """
    將defect圖依據瑕疵種類(檔名的最後一個字母)分到資料夾
    defect圖檔名格式: defect圖的檔名格式為 桿頭編號-面向_xmin_ymin_xmax_ymax_類別(eg. 20210923134554SM-A_D171_9_TOTAL_V0-CROWN1_337_449_348_458_A)

    Args:
        cropSetPath: 要切分類別資料夾的路徑，其下包含defect圖
    """
    print("Dividing data to each class folder ...")

    for resultFolder in cropSetPath:
        print("In {} directory".format(resultFolder))
        for file in os.listdir(resultFolder):
            if not os.path.isdir(os.path.join(resultFolder, file.split('_')[-1][:-4])):
                os.mkdir(os.path.join(resultFolder, file.split('_')[-1][:-4]))
                print("- Create new folder : {}".format(file.split('_')[-1][:-4]))
            if len(file) == 1:
                continue
            shutil.move(os.path.join(resultFolder, file), os.path.join(resultFolder, file.split('_')[-1][:-4], file))



if __name__ == '__main__':
    # xml_path = './data/0825/RawData/2048x2048_RawData/Xml/'
    RAW_DATA_PATH = './data/0923/CropROI_1536x1536/Image'
    TXT_PATH = './data/0923/data_segment/'
    ANNOTATION_PATH = './data/0923/CropROI_1536x1536/Annotation/Txt_BBox/'
    OUTPUT_PATH = './FirstPhaseData' 
    CLASS_NAME = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'FP']
    DATASET = ['test', 'train', 'valid']
    '''
    RAW_DATA_PATH   : 原始影像的路徑
    TXT_PATH        : 此路徑下須包括train, valid, test三個txt檔(檔名格式範例 : Test_0923_train)，txt中為各dataset的檔名列表
    ANNOTATION_PATH : annotation的路徑，路徑下須包括所有影像的annotation txt檔，檔名會與RAW_DATA_PATH下的檔名一一對應
    xml_path        : 若annotation是xml格式，則需給予xml檔的路徑
    OUTPUT_PATH     : 結果輸出的路徑
    CLASS_NAME      : 類別名稱
    DATASET         : 要切那些資料集，與txt檔對應，e.g.只要切test和train兩種資料集，則DATASET = ['test', 'train'], TXT_PATH路徑下需有Test_0923_test及Test_0923_train兩個txt檔
    若要單獨使用crop_defect_fromtxt()或是classfolder_divide()，需額外定義路徑dataset_path或是cropSetPath，資料型態為list
    '''

    ##### Classification preprocessing #####
    dataset_path = dataset_divide(TXT_PATH, RAW_DATA_PATH, OUTPUT_PATH, DATASET)
    cropSetPath = crop_defect_fromtxt(ANNOTATION_PATH, dataset_path, OUTPUT_PATH, DATASET, CLASS_NAME)
    # crop_defect_fromxml(xml_path, OUTPUT_PATH, DATASET)
    classfolder_divide(cropSetPath)
    
    