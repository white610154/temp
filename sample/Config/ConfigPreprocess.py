class PreprocessPara:
    normalize    = {"switch": False, "mode": 'ImageNet', "mean": None, "std": None}
    resize       = {"switch": False, "imageSize":[224, 224], "interpolation": 'BILINEAR'}
    centerCrop   = {"switch": False, "size": [1, 1]}
    pad          = {"switch": False, "padding": [0, 0, 0, 0], "fill": [0, 0, 0], "paddingMode": 'constant'}
    gaussianBlur = {"switch": False, "kernelSize": [1, 1], "sigma": 1}
    brightness   = {"switch": False, "brightness": 1}
    contrast     = {"switch": False, "contrast": 1}
    saturation   = {"switch": False, "saturation": 1}
    hue          = {"switch": False, "hue": 0}