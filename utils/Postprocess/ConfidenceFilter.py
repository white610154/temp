import torch

def confidence_threshold(outputs, className, selectLabel:str, confidenTh:float):
    '''
    If the prediction is selectLabel which has the confidence lower than confidenTh, reduce the confidence to 0

    Args:
        output: original logits from model output
        className: the class name list which is corresponding to model output nodes
        selectLabel: the class which need to be filtered
        confidenTh: confidence threshold
        
    Return:
        newOutput: new output logits after confidence_threshold filter
    '''
    outputsSoftmax = torch.nn.functional.softmax(outputs, dim=1)
    confidenceScore, predicted = torch.max(outputsSoftmax, 1)
    confidenLabelNumber = None
    for i in range(len(className)):
        if className[i] == selectLabel:
            confidenLabelNumber = i   # obtain selectLabel index in the className
    assert isinstance(confidenLabelNumber, int), f'you selected label: "{selectLabel}" does not exit, model label: {className}'
    
    if predicted[0] == confidenLabelNumber and confidenceScore[0] < confidenTh:  
        print(f'{className[confidenLabelNumber]}\'s sorce is {confidenceScore[0]}, and it has been filtered out')
        outputs[0][confidenLabelNumber] = 0 

    return outputs