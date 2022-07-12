class AugmentationPara:
    randomHorizontalFlip = {"switch": False, "probability": 0.5}
    randomVerticalFlip = {"switch": False, "probability": 0.5}
    randomRotation = {"switch": False, "degrees": [-360, 360], "fill": [0, 0, 0]}
    randomTranslate = {"switch": False, "translate": [0, 0], "fill": [0, 0, 0]}
    randomScale = {"switch": False, "scale": [1, 1], "fill": [0, 0, 0]}
    randomShear = {"switch": False, "shear": [0, 0, 0, 0], "fill": [0, 0, 0]}
    randomGrayscale = {"switch": False, "probability": 0.5}
    randomBrightness = {"switch": False, "brightness": [1, 1]}
    randomContrast = {"switch": False, "contrast": [1, 1]}
    randomSaturation = {"switch": False, "saturation" :[1, 1]}
    randomHue = {"switch": False, "hue": [0, 0]}
    randomErasing = {"switch": False, "probability": 0.5, "scale": [0.02, 0.33], "ratio": [0.3, 3.3], "value": [0, 0, 0]}
    randomPerspective = {"switch": False, "distortion" : 0, "probability": 0.5, "interpolation": "BILINEAR", "fill": [0, 0, 0]}