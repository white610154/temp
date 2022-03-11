from config.ConfigPostprocess import PostProcessPara
from .ConfidenceFilter import confidence_threshold

def select_postprocess(outputs, className):
    """
    According to configs in ConfigPostprocess, select the post processing method.

    Args:
        outputs: logits from model output
        className: list of all class name
    Return:
        outputs: new logits after post processing
    """
    className.sort()
    className.sort(key=lambda x:x)

    if PostProcessPara.confidenceFilter['switch']:
        outputs = confidence_threshold(outputs, className, PostProcessPara.confidenceFilter['selectLabel'], PostProcessPara.confidenceFilter['threshold'])
    return outputs