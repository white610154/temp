class PreprocessPara:
    normalize    = {"switch": False,  "mode": 0, "mean": [0.5, 0.5, 0.5], "std": [0.5, 0.5, 0.5]}
    resize       = {"switch": False,  "imageSize":[1, 1], "interpolation": 'BILINEAR'}
    centerCrop   = {"switch": False, "size": [1, 1]}
    pad          = {"switch": False, "padding": [0, 0, 0, 0], "fill": [0, 0, 0], "paddingModel": 'constant'}
    gaussianBlur = {"switch": False, "kernelSize": [1, 1], "sigma": 0}
    brightness   = {"switch": False, "brightness": 1}
    contrast     = {"switch": False, "contrast": 1}
    saturation   = {"switch": False, "saturation": 1}
    hue          = {"switch": False, "hue": 0}