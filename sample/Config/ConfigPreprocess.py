class PreprocessPara:
    normalize    = {"switch": True,  "mode": 1, "mean": [], "std": []}
    resize       = {"switch": True,  "imageSize":[224, 224], "interpolation": 'BILINEAR'}
    centerCrop   = {"switch": False, "size": [100, 100]}
    pad          = {"switch": False, "padding": [3, 3], "fill": (0, 255, 0), "paddingModel": 'constant'}
    gaussianBlur = {"switch": False, "kernelSize": [3, 3], "sigma": 0.1}
    brightness   = {"switch": False, "brightness": 0}
    contrast     = {"switch": False, "contrast": 0}
    saturation   = {"switch": False, "saturation": 0}
    hue          = {"switch": False, "hue": 0}