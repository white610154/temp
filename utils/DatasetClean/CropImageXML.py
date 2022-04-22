import os, cv2, csv
import xml.etree.ElementTree as ET


path = './2048_xml/'
filelist = os.listdir(path)


for filename in filelist:
    if filename[-4:] == '.jpg':
        cnt = 0
        img = cv2.imread(path + filename)
        tree = ET.parse(path + filename[:-4] + '.xml')
        root = tree.getroot()        
        for obj in root.findall('object'):
            name = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            xmax = bndbox.find('xmax').text
            ymax = bndbox.find('ymax').text

            ###### generate label ######
            # with open('label_1cls.csv', 'a', newline='') as csvfile:
            #     writer = csv.writer(csvfile)
            #     cls_list = []
            #     cls_list.append(filename)
            #     cls_list.append(name)                
            #     writer.writerow(cls_list)
            #     print(cls_list)
            ###### generate label ######

            ###### show bbox ######
            # cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
            ###### show bbox ######

            ###### crop defect ######
            # xcenter = (int(xmax) + int(xmin)) / 2
            # ycenter = (int(ymax) + int(ymin)) / 2
            # print(int(xcenter), int(ycenter), name)
            # xhead = int(xcenter) - 350
            # xtail = int(xcenter) + 350 - 1
            # yhead = int(ycenter) - 350
            # ytail = int(ycenter) + 350 - 1
            # if xhead <= 0:
            #     xhead = 0
            #     xtail = 699
            # elif xtail >= 2047:
            #     xhead = 1348
            #     xtail = 2047
            # if yhead <= 0:
            #     yhead = 0
            #     ytail = 699
            # elif ytail >= 2047:
            #     yhead = 1348
            #     ytail = 2047
            # crop_img = img[yhead : ytail, xhead : xtail]
            # print('./crop/' + filename[:-4] + '_' + str(cnt) + '_' + name + '.jpg')
            # cv2.imwrite('./crop/' + filename[:-4] + '_' + str(cnt) + '_' + name + '.jpg', crop_img)
            # cnt = cnt + 1
            # cv2.imshow('crop_img', crop_img)
            # cv2.waitKey()
            ###### crop defect ######