import torch
from config.ConfigPostprocess import PostProcessPara

class PostProcess:
    def __init__(self, outputs, className=None):
        self.outputs = outputs
        self.className = className
    
    def select_process(self):
        if PostProcessPara.confidenceFilter['switch']:
            self.outputs = self.confidence_threshold(PostProcessPara.confidenceFilter['selectLabel'], PostProcessPara.confidenceFilter['threshold'])
        return self.outputs

    def confidence_threshold(self, selectLabel:str, confidenTh:float):
        '''
            過濾指定類別(selectLabel)希望信心分數高於門檻(confidenTh)，否則選擇次高的結果，輸出最高分數的結果

            Args:
                output: 模型原本輸出的結果
                className: 按照模型順序的類別名稱
                selectLabel: 選擇要卡分數的類別
                confidenTh: 信心分數門檻值
                
            Return:
                newOutput: 過濾過的新輸出結果
        '''
        outputsSoftmax = torch.nn.functional.softmax(self.outputs, dim=1)
        confidenceScore, predicted = torch.max(outputsSoftmax, 1)
        confidenLabelNumber = None
        for i in range(len(self.className)):
            if self.className[i] == selectLabel:
                confidenLabelNumber = i   # 紀錄指定類別的位置
        assert isinstance(confidenLabelNumber, int), f'you selected label: "{selectLabel}" does not exit, model label: {self.className}'
        
        if predicted[0] == confidenLabelNumber and confidenceScore[0] < confidenTh:  
            print(f'{self.className[confidenLabelNumber]}\'s sorce is {confidenceScore[0]}, and it has been filtered out')
            self.outputs[0][confidenLabelNumber] = 0  #把原本最高分數改成0
        newOutput = self.outputs

        return newOutput


    # def bright_enhance(image, brightness=0.8):
    #     enhBri = ImageEnhance.Brightness(image)
    #     newImg = enhBri.enhance(brightness)

    #     return newImg

    # def contrast_enhance(image, contrast = 2):
    #     newImg = ImageEnhance.Contrast(image).enhance(contrast)  
    #     return newImg

    # def color_sharp(image, factor=2):
    #     enh_sha = ImageEnhance.Sharpness(image)
    #     newImg = enh_sha.enhance(factor=1.5)
    #     return newImg

    # def get_sketch(image):
    #     return image.filter(CONTOUR)

    # def rotate(image, angle=90):
    #     if angle == 90:
    #         newImg = image.transpose(Image.ROTATE_90)
    #     if angle == 180:
    #         newImg = image.transpose(Image.ROTATE_180)
    #     if angle == 270:
    #         newImg = image.transpose(Image.ROTATE_270)
    #     return newImg

    # def post_process(label, confidence:tensor, outputs, filePath, count, model, transform, device):
    #     for i in range(len(confidence)):
    #         topConf, topIndx = torch.topk(confidence[i], 2)
            
    #         fileName = str(filePath[count])
    #         topIndx = topIndx.tolist()
    #         image = Image.open(filePath[count]).convert('RGB')

    #         #### For v17 epoch-250 #####
    #         if topIndx[0] == 3 and image.size[0] < 100 and image.size[1] < 100:
    #             # print("{}, label:{}, TopInd:{}, TopConf:{}, size:{}, {}".format(fileName.split('\\')[-1], int(label[i]), topIndx, topConf, image.size, outputs[i]))
    #             index = [0, 3, 2, 1, 4, 5]
    #             outputs[i] = outputs[i][index]


    #         if topIndx[0] == 1 and topIndx[1] == 0:
    #             # print("{}, label:{}, TopInd:{}, TopConf:{}, size:{}, {}".format(fileName.split('\\')[-1], int(label[i]), topIndx, topConf, image.size, outputs[i]))
    #             image = bright_enhance(image, brightness=0.8)
    #             image = transform(image)
    #             newImage = image.to(device).unsqueeze(0)
    #             outputs[i] = model(newImage)
            
    #         if  topIndx[0] == 5:
    #             # print("{}, label:{}, TopInd:{}, TopConf:{}, size:{}, {}".format(fileName.split('\\')[-1], int(label[i]), topIndx, topConf, image.size, outputs[i]))
    #             image = bright_enhance(image, brightness=0.8)
                
    #             image = transform(image)
    #             newImage = image.to(device).unsqueeze(0)
    #             outputs[i] = model(newImage)
            
    #         if topIndx[0] == 0 and topIndx[1] == 1 and topConf[0] < topConf[1] * 10:
    #             # print("{}, label:{}, TopInd:{}, TopConf:{}, size:{}, {}".format(fileName.split('\\')[-1], int(label[i]), topIndx, topConf, image.size, outputs[i]))
    #             image = bright_enhance(image, brightness=0.8)
                
    #             image = transform(image)
    #             newImage = image.to(device).unsqueeze(0)
    #             outputs[i] = model(newImage)
    #         count += 1
    #     confidence = torch.nn.functional.softmax(outputs, dim=1)
    #     return count, outputs, confidence