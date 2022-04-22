import shutil, os, cv2
import numpy as np

from PIL import Image

class CropTrain():
    def __init__(self, dataPath, labelPath, state, **kwargs):
        print(dataPath, labelPath, state)
        if state == 0:
            pass
        else:
            print(" - The data don't need cropping.")

    def crop_defect_fromtxt(self, annotation_path:str, dataset_path: list, output_path:str, dataset:list, className:list):
        """
        將資料夾下的原始圖片依據txt所記錄的Bbox座標切出defect，並存到output_path的crop資料夾中
        defect圖的檔名格式為 桿頭編號-面向_xmin_ymin_xmax_ymax_類別(eg. 20210923134554SM-A_D171_9_TOTAL_V0-CROWN1_337_449_348_458_A)

        Args:
            annotation_path: annotation檔的路徑，路徑下為所有的txt檔，檔名與圖片的檔名對應
            dataset_path: 要切出defect的目標資料夾，下含要切defect的原始圖片
            output_path: 輸出切分結果的路徑，切好defect的圖會存在其下的crop資料夾
            dataset: 要切分的資料集種類，與txt檔數量相同
            className: 要切分的defect種類

        Return:
            cropSetPath: 要切分類別資料夾的路徑，其下包含defect圖
        """
        print("- Cropping defect according to txt file ...")
        
        className.sort()
        className.sort(key=lambda x:x)

        cropSetPath = []
        for i, name in enumerate(dataset):
            resultFolder = os.path.join(output_path, 'cleaned_' + name)
            cropSetPath.append(resultFolder)
            if not os.path.isdir(resultFolder):
                os.makedirs(resultFolder)

            fileList = os.listdir(dataset_path[i])

            total_class = 0
            total_data = 0
            for fileName in fileList:
                # print(fileName)
                f = open(os.path.join(annotation_path, fileName[:-4] + '.txt'), 'r')
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

            print("  - {} set has {} classes, total data : {}".format(name, total_class + 1, total_data))
        
        return cropSetPath
    
        

# class inference():
#     def __init__(self):
#         if ClsDataCleanPara.data_clean:
#             self.crop_defect_fromcsv(ClsDataCleanPara.csv_path, ClsDataCleanPara.image_path, ClsDataCleanPara.output_path, ClsDataCleanPara.confidence_thres)
#         else:
#             print('- The data have been cleaned up')

#     def crop_defect_fromcsv(self, csv_path:str, image_path:str, output_path:str, confidence_thres:float):
#         """
#         依據phase1的結果 (csv file) 從原圖中框出defect存成圖檔
        
#         Args:
#             csv_path: detection的結果，須為csv檔
#             image_path: 原圖的路徑
#             output_path: 結果輸出的路徑
#             confidence_thres: detection confidence的閥值，可去除confidence太低的detection結果
#         """
#         print("- Cropping defect from csv file ...")
#         if not os.path.isdir(output_path):
#             os.makedirs(output_path)
#         flag = 0
#         with open(csv_path, newline='') as csvfile:
#             rows = csv.reader(csvfile)
#             for row in rows:
#                 if flag == 0:
#                     flag += 1
#                     continue
#                 if float(row[7]) < confidence_thres:
#                     continue
#                 img = cv2.imread(os.path.join(image_path, row[0]))
#                 # print(row)
#                 # print(int(row[4]), int(row[6]), int(row[3]) , int(row[5]))
#                 # cv2.imshow('show_image', img)
#                 # cv2.waitKey(0)
#                 cropImg = img[int(row[4]) : int(row[6]), int(row[3]) : int(row[5])]
#                 resultPath = os.path.join(output_path, row[0][:-4] + '_' + row[3] + '_' + row[4] + '_' + row[5] + 
#                             '_' + row[6] + '_' + row[7] + '_' + row[2] +  '.jpg')
#                 cv2.imwrite(resultPath, cropImg)

    