import matplotlib.pyplot as plt
import itertools
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator

def draw_acc_curve(accRecord:list, outputPath:str) -> None:
    """
    Draw accuracy curve.

    Args:
        accRecord: a list including validation accuracy of all epochs

    Return:
        ValidAcc.jpg
    """
    epochRecord = list(range(1, len(accRecord)+1))
    plt.plot(epochRecord, accRecord, color='blue')
    plt.title('accuracy curve')
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.legend(['acc'], loc='upper left')
    plt.grid()
    plt.savefig(f'./{outputPath}/ValidAcc.jpg')
    # plt.show()


def plot_confusion_matrix(cfMatrix, className:list, showNumber:bool=False, title:str='Confusion matrix', outputPath:str='./') -> None:
    ### 阿阿阿世亞我普吉島cfMatrix是什麼型態, 雙重陣列type?
    """
    This function prints and plots the confusion matrix.

    Args:
        cfMatrix: 2D confusion matrix
        className: class name
        showNumber: True: show in number
        title: title of the figure
    """
    cm = cfMatrix.copy()
    cm = np.array(cm, dtype='uint32')
    # print(cm)
    fig = plt.figure()
    cells = cm.flatten()
    cmRowNorm = cm / cm.sum(axis=1)[:, np.newaxis]
    rowPercentages = ["{0:.2f}".format(value) for value in cmRowNorm.flatten()]
    
    if showNumber:
        cellTexts = [f"{cnt}\n{per}" for cnt, per in zip(cells, rowPercentages)]
    else:
        cellTexts = [f"{per}" for per in rowPercentages]
    cellTexts = np.asarray(cellTexts).reshape(cm.shape[0], cm.shape[1])
    
    cmDataframe = pd.DataFrame(cmRowNorm, index=className, columns=className)
    hmap = sns.heatmap(cmDataframe, annot=cellTexts, fmt="", cmap="Greens")
    hmap.yaxis.set_ticklabels(hmap.yaxis.get_ticklabels(), rotation=0, ha='right')
    hmap.xaxis.set_ticklabels(hmap.xaxis.get_ticklabels(), rotation=30, ha='right')
    
    plt.title(title)
    plt.ylabel('Label')
    plt.xlabel('Predict')
    fig.savefig(f'./{outputPath}/ConfusionMatrix.jpg', dpi=fig.dpi, bbox_inches='tight')

    # if normalize:
    #     cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    # plt.imshow(cm, interpolation='nearest', cmap=cmap)
    # plt.title(title)
    # plt.colorbar()
    # tick_marks = np.arange(len(classesName))
    # plt.xticks(tick_marks, classesName, rotation=45)
    # plt.yticks(tick_marks, classesName)

    # fmt = '.2f' if normalize else 'd'
    # thresh = cm.max() / 2.
    # print(cm)
    # for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    #     plt.text(j, i, cm[i, j],
    #             horizontalalignment='center',
    #             color='white' if cm[i, j] > thresh else 'black')
    # plt.ylabel('True label')
    # plt.xlabel('Predicted label')
    # plt.tight_layout()
    # plt.savefig(f'./{PrivateSetting.outputPath}/ConfusionMatrix.jpg')
    # plt.show()
