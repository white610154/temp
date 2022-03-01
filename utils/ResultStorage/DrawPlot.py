import matplotlib.pyplot as plt
import itertools
import numpy as np
from config.Config import BasicSetting, PrivateSetting
from config.ConfigResultStorage import ResultStorage

def draw_acc_curve(accRecord:list):
    """
    Draw accuracy curve.

    Args:
        accRecord:包含每個epoch的testing data準確率
    """
    if ResultStorage.drawAccCurve:
        plt.plot(accRecord, color='blue')
        plt.title('accuracy curve')
        plt.ylabel('acc')
        plt.xlabel('epoch')
        plt.legend(['acc'], loc='upper left')
        plt.grid()
        plt.savefig(f'./{PrivateSetting.outputPath}/ValidAccCurve.jpg')
        # plt.show()


def plot_confusion_matrix(cm, classes:list, normalize:bool=True, title:str='Confusion matrix', cmap=plt.cm.Greens):
    """
    This function prints and plots the confusion matrix.

    Args:
        cm: 2維的confusion matrix
        classes: 類別名稱
        normalize: True:以比例值顯示
        title: 圖示的標題
        cmap: 顏色
    """
    if ResultStorage.drawConfusionMatrix:
        print(cm)
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.

        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()
        plt.savefig(f'./{PrivateSetting.outputPath}/ConfusionMatrix.jpg')
        # plt.show()
