class AugmentationPara:
    randomHorizontalFlip = {"switch": True,  "probability": 0.5}
    randomVerticalFlip   = {"switch": False, "probability": 0.5}
    randomRotation       = {"switch": False, "degress"    : [30, 70]}
    randomTranslate      = {"switch": False, "translate"  : [0.1, 0.3]}
    randomScale          = {"switch": False, "scale"      : [0.5, 0.75]}
    randomShear          = {"switch": False, "shear"      : [0.0, 0.0, 0.0, 0.0]}
    randomGrayscale      = {"switch": False, "probability": 0.1}
    randomBrightness     = {"switch": False, "brightness" : [1.0, 1.0]}
    randomContrast       = {"switch": False, "contrast"   : [2.0, 2.0]}
    randomSaturation     = {"switch": False, "saturation" : [3.0, 4.0]}
    randomHue            = {"switch": False, "hue"        : [-0.1, 0.1]}
    randomErasing        = {"switch": False, "probability": 0.5, "scale": [0.02, 0.33], "ratio": [0.3, 3.3], "value": [0, 0, 0]}
    randomPerspective    = {"switch": False, "distortion" : 0.5, "probability": 0.5, "interpolation": "BILINEAR", "fill": [0, 0, 0]}