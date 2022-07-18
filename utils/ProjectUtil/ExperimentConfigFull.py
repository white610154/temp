config = {
    "ConfigPreprocess": {
        "PreprocessPara": {
            "normalize": {
                "description": "將根據輸入模式找到對應各通道的平均、標準差，進行影像正規化",
                "mode": {
                    "type": "string",
                    "default": "ImageNet",
                    "enums": {
                        "ImageNet": "ImageNet",
                        "CIFAR10": "CIFAR10",
                        "MNIST": "MNIST",
                        "CalculateFromData": "CalculateFromData",
                        "UserInput": "UserInput"
                    }
                },
                "mean": {
                    "type": "list",
                    "children": {
                        "R": {
                            "type": "float",
                            "default": 0.5,
                            "min": 0,
                            "max": 1
                        },
                        "G": {
                            "type": "float",
                            "default": 0.5,
                            "min": 0,
                            "max": 1
                        },
                        "B": {
                            "type": "float",
                            "default": 0.5,
                            "min": 0,
                            "max": 1
                        },
                    },
                    "nullable": True
                },
                "std": {
                    "type": "list",
                    "children": {
                        "R": {
                            "type": "float",
                            "default": 0.5,
                            "min": 0,
                            "max": 1
                        },
                        "G": {
                            "type": "float",
                            "default": 0.5,
                            "min": 0,
                            "max": 1
                        },
                        "B": {
                            "type": "float",
                            "default": 0.5,
                            "min": 0,
                            "max": 1
                        },
                    },
                    "nullable": True
                }
            },
            "resize": {
                "description": "調整影像大小至給定的數值",
                "imageSize": {
                    "type": "list",
                    "children": {
                        "width": {
                            "type": "int",
                            "default": 224,
                            "min": 1,
                            "unit": "pixels"
                        },
                        "height": {
                            "type": "int",
                            "default": 224,
                            "min": 1,
                            "unit": "pixels"
                        },
                    },
                },
                "interpolation": {
                    "type": "string",
                    "default": "BILINEAR",
                    "enums": {
                        "BILINEAR": "BILINEAR",
                        "NEAREST": "NEAREST",
                        "BICUBIC": "BICUBIC"
                    }
                }
            },
            "centerCrop": {
                "description": "以影像中心點切出給定數值大小的影像",
                "size": {
                    "type": "list",
                    "children": {
                        "width": {
                            "type": "int",
                            "default": 1,
                            "min": 0,
                            "unit": "pixels"
                        },
                        "height": {
                            "type": "int",
                            "default": 1,
                            "min": 0,
                            "unit": "pixels"
                        },
                    },
                }
            },
            "pad": {
                "description": "向外進行影像填充",
                "padding":  {
                    "type": "list",
                    "children": {
                        "left": {
                            "type": "int",
                            "default": 0,
                            "min": 0,
                            "unit": "pixels"
                        },
                        "top": {
                            "type": "int",
                            "default": 0,
                            "min": 0,
                            "unit": "pixels"
                        },
                        "right": {
                            "type": "int",
                            "default": 0,
                            "min": 0,
                            "unit": "pixels"
                        },
                        "bottom": {
                            "type": "int",
                            "default": 0,
                            "min": 0,
                            "unit": "pixels"
                        }
                    }
                },
                "fill": {
                    "type": "list",
                    "children": {
                        "R": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "G": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "B": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        }
                    },
                    "nullable": True
                },
                "paddingMode": {
                    "type": "string",
                    "default": "constant",
                    "enums": {
                        "constant": "constant",
                        "edge": "edge",
                        "reflect": "reflect",
                        "symmetric": "symmetric",
                    }
                }
            },
            "gaussianBlur": {
                "description": "對影像做高斯模糊",
                "kernelSize":
                {
                    "type": "list",
                    "children": {
                        "width": {
                            "type": "int",
                            "default": 3,
                            "min": 1,
                            "unit": "pixels"
                        },
                        "height": {
                            "type": "int",
                            "default": 3,
                            "min": 1,
                            "unit": "pixels"
                        }
                    }
                },
                "sigma": {
                    "type": "float",
                    "default": 1,
                    "min": 0
                }
            },
            "brightness": {
                "description": "對影像做亮度調整",
                "brightness": {
                    "type": "float",
                    "default": 1,
                    "min": 0,
                    "max": 5,
                }
            },
            "contrast": {
                "description": "對影像做對比度調整",
                "contrast": {
                    "type": "float",
                    "default": 1,
                    "min": 0,
                    "max": 5,
                }
            },
            "saturation": {
                "description": "對影像做飽和度調整",
                "saturation": {
                    "type": "float",
                    "default": 1,
                    "min": 0,
                    "max": 5,
                }
            },
            "hue": {
                "description": "對影像做色調調整",
                "hue": {
                    "type": "float",
                    "default": 0,
                    "max": 0.5,
                    "min": -0.5
                }
            }
        }
    },
    "ConfigAugmentation": {
        "AugmentationPara": {
            "randomHorizontalFlip": {
                "description": "以給定的機率隨機對影像做水平翻轉",
                "probability": {
                    "type": "float",
                    "default": 0.5,
                    "max": 1,
                    "min": 0
                }
            },
            "randomVerticalFlip": {
                "description": "以給定的機率隨機對影像做垂直翻轉",
                "probability": {
                    "type": "float",
                    "default": 0.5,
                    "max": 1,
                    "min": 0
                }
            },
            "randomRotation": {
                "description": "在給定角度範圍內隨機對影像做旋轉",
                "degrees": {
                    "type": "list",
                    "children": {
                        "min": {
                            "type": "float",
                            "default": -360,
                            "max": 360,
                            "min": -360,
                            "unit": "degrees"
                        },
                        "max": {
                            "type": "float",
                            "default": 360,
                            "max": 360,
                            "min": -360,
                            "unit": "degrees"
                        }
                    }
                },
                "fill": {
                    "type": "list",
                    "children": {
                        "R": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "G": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "B": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        }
                    },
                    "nullable": True
                }
            },
            "randomTranslate": {
                "description": "在給定平移範圍內隨機對影像做平移",
                "translate": {
                    "type": "list",
                    "children": {
                        "horizontalRatio": {
                            "type": "float",
                            "default": 0,
                            "max": 1,
                            "min": 0
                        },
                        "verticalRatio": {
                            "type": "float",
                            "default": 0,
                            "max": 1,
                            "min": 0
                        }
                    }
                },
                "fill": {
                    "type": "list",
                    "children": {
                        "R": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "G": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "B": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        }
                    },
                    "nullable": True
                }
            },
            "randomScale": {
                "description": "在給定縮放範圍內隨機對影像做縮放",
                "scale": {
                    "type": "list",
                    "children": {
                        "horizontalRatio": {
                            "type": "float",
                            "default": 1,
                            "max": 5,
                            "min": 0,
                            "unit": "degrees"
                        },
                        "verticalRatio": {
                            "type": "float",
                            "default": 1,
                            "max": 5,
                            "min": 0,
                            "unit": "degrees"
                        }
                    }
                },
                "fill": {
                    "type": "list",
                    "children": {
                        "R": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "G": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "B": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        }
                    },
                    "nullable": True
                }
            },
            "randomShear": {
                "description": "在給定斜變範圍內隨機以軸對影像做斜變",
                "shear": {
                    "type": "list",
                    "children": {
                        "horizontalDegreeMin": {
                            "type": "float",
                            "default": -360,
                            "max": 360,
                            "min": -360,
                            "unit": "degrees"
                        },
                        "horizontalDegreeMax": {
                            "type": "float",
                            "default": 360,
                            "max": 360,
                            "min": -360,
                            "unit": "degrees"
                        },
                        "verticalDegreeMin": {
                            "type": "float",
                            "default": -360,
                            "max": 360,
                            "min": -360,
                            "unit": "degrees"
                        },
                        "verticalDegreeMax": {
                            "type": "float",
                            "default": 360,
                            "max": 360,
                            "min": -360,
                            "unit": "degrees"
                        }
                    }
                },
                "fill": {
                    "type": "list",
                    "children": {
                        "R": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "G": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "B": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        }
                    },
                    "nullable": True
                }
            },
            "randomGrayscale": {
                "description": "以給定的機率隨機對影像做灰階轉換",
                "probability": {
                    "type": "float",
                    "default": 0.5,
                    "max": 1,
                    "min": 0
                }
            },
            "randomBrightness": {
                "description": "在給定亮度範圍內隨機對影像做亮度調整",
                "brightness": {
                    "type": "list",
                    "children": {
                        "min": {
                            "type": "float",
                            "default": 1,
                            "min": 0,
                            "max": 5
                        },
                        "max": {
                            "type": "float",
                            "default": 1,
                            "min": 0,
                            "max": 5
                        }
                    }
                }
            },
            "randomContrast": {
                "description": "在給定對比度範圍內隨機對影像對比度調整",
                "contrast": {
                    "type": "list",
                    "children": {
                        "min": {
                            "type": "float",
                            "default": 1,
                            "min": 0,
                            "max": 5
                        },
                        "max": {
                            "type": "float",
                            "default": 1,
                            "min": 0,
                            "max": 5
                        }
                    }
                }
            },
            "randomSaturation": {
                "description": "在給定飽和度範圍內隨機對影像做飽和度調整",
                "saturation": {
                    "type": "list",
                    "children": {
                        "min": {
                            "type": "float",
                            "default": 1,
                            "min": 0,
                            "max": 5
                        },
                        "max": {
                            "type": "float",
                            "default": 1,
                            "min": 0,
                            "max": 5
                        }
                    }
                }
            },
            "randomHue": {
                "description": "在給定色調範圍內隨機對影像做色調調整",
                "hue": {
                    "type": "list",
                    "children": {
                        "min": {
                            "type": "float",
                            "default": 0,
                            "max": 0.5,
                            "min": -0.5,
                        },
                        "max": {
                            "type": "float",
                            "default": 0,
                            "max": 0.5,
                            "min": -0.5,
                        }
                    }
                }
            },
            "randomErasing": {
                "description": "在給定範圍內產生一個矩形，隨機對影像做遮罩",
                "probability": {
                    "type": "float",
                    "default": 0.5,
                    "max": 1,
                    "min": 0
                },
                "scale": {
                    "type": "list",
                    "children": {
                        "min": {
                            "type": "float",
                            "default": 0.02,
                            "max": 1,
                            "min": 0,
                        },
                        "max": {
                            "type": "float",
                            "default": 0.33,
                            "max": 1,
                            "min": 0,
                        }
                    },
                    "display": "erasingSizeRatio"
                },
                "ratio": {
                    "type": "list",
                    "children": {
                        "min": {
                            "type": "float",
                            "default": 0.3,
                            "min": 0,
                            "max": 5
                        },
                        "max": {
                            "type": "float",
                            "default": 3.3,
                            "min": 0,
                            "max": 5
                        }
                    },
                    "display": "lengthWidthRatio"
                },
                "value": {
                    "type": "list",
                    "children": {
                        "R": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "G": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "B": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        }
                    },
                    "display": "fill"
                }
            },
            "randomPerspective": {
                "description": "以給定的機率隨機對影像做視角轉換",
                "distortion": {
                    "type": "float",
                    "default": 0,
                    "max": 1,
                    "min": 0
                },
                "probability": {
                    "type": "float",
                    "default": 0.5,
                    "max": 1,
                    "min": 0
                },
                "interpolation": {
                    "type": "string",
                    "default": "BILINEAR",
                    "enums": {
                        "BILINEAR": "BILINEAR",
                        "NEAREST": "NEAREST",
                        "BICUBIC": "BICUBIC"
                    }
                },
                "fill": {
                    "type": "list",
                    "children": {
                        "R": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "G": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        },
                        "B": {
                            "type": "int",
                            "default": 0,
                            "max": 255,
                            "min": 0,
                        }
                    }
                }
            }
        }
    },
    "ConfigModelService": {
        "LossFunctionPara": {
            "lossFunction": {
                "type": "string",
                "default": "CrossEntropyLoss",
                "enums": {
                    "CrossEntropyLoss": "CrossEntropyLoss",
                    "NLLLoss": "NLLLoss",
                    "MultiMarginLoss": "MultiMarginLoss",
                }
            }
        },
        "LearningRate": {
            "learningRate": {
                "type": "float",
                "default": 0.001,
                "min": 0
            }
        },
        "OptimizerPara": {
            "SGD": {
                "momentum": {
                    "type": "float",
                    "default": 0.9,
                    "max": 1,
                    "min": 0
                },
                "dampening": {
                    "type": "float",
                    "default": 0,
                    "max": 1,
                    "min": 0
                },
                "weightDecay": {
                    "type": "float",
                    "default": 5e-4,
                    "max": 1,
                    "min": 0
                },
                "nesterov": {
                    "type": "boolean",
                    "default": False
                }
            },
            "Adam": {
                "betas": {
                    "type": "list",
                    "children": {
                        "min": {
                            "type": "float",
                            "default": 0.9,
                            "max": 1,
                            "min": 0,
                        },
                        "max": {
                            "type": "float",
                            "default": 0.999,
                            "max": 1,
                            "min": 0,
                        },
                    }
                },
                "eps": {
                    "type": "float",
                    "default": 1e-8,
                    "max": 1,
                    "min": 0
                },
                "weightDecay": {
                    "type": "float",
                    "default": 0,
                    "max": 1,
                    "min": 0
                },
                "amsgrad": {
                    "type": "boolean",
                    "default": False
                }
            },
            "Adadelta": {
                "rho":  {
                    "type": "float",
                    "default": 0.9,
                    "max": 1,
                    "min": 0
                },
                "eps": {
                    "type": "float",
                    "default": 1e-6,
                    "max": 1,
                    "min": 0
                },
                "weightDecay": {
                    "type": "float",
                    "default": 0,
                    "max": 1,
                    "min": 0
                }
            },
            "AdamW": {
                "betas": {
                    "type": "list",
                    "children": {
                        "min": {
                            "type": "float",
                            "default": 0.9,
                            "max": 1,
                            "min": 0,
                        },
                        "max": {
                            "type": "float",
                            "default": 0.999,
                            "max": 1,
                            "min": 0,
                        },
                    }
                },
                "eps": {
                    "type": "float",
                    "default": 1e-8,
                    "max": 1,
                    "min": 0
                },
                "weightDecay": {
                    "type": "float",
                    "default": 0.01,
                    "max": 1,
                    "min": 0
                },
                "amsgrad": {
                    "type": "boolean",
                    "default": False
                }
            },
        },
        "SchedulerPara": {
            "stepLR": {
                "stepSize": {
                    "type": "int",
                    "default": 10,
                    "min": 1
                },
                "gamma": {
                    "type": "float",
                    "default": 0.1
                }
            },
            "cosineAnnealingLR": {
                "tMax": {
                    "type": "int",
                    "min": 1
                },
                "etaMin": {
                    "type": "float",
                    "default": 0,
                    "min": 0
                }
            }
        }
    },
    "ConfigPytorchModel": {
        "SelectedModel": {
            "model": {
                "structure": {
                    "type": "string",
                    "default": "auo_unrestricted_powerful_model",
                    "enums": {
                        "auo_tiny_focus_model": "auo_tiny_focus_model",
                        "auo_classic_deep_model": "auo_classic_deep_model",
                        "auo_anti_degeneration_model": "auo_anti_degeneration_model",
                        "auo_transform_aggregate_model": "auo_transform_aggregate_model",
                        "auo_narrow_intensive_model": "auo_narrow_intensive_model",
                        "auo_feature_enhance_model_a": "auo_feature_enhance_model_a",
                        "auo_feature_enhance_model_b": "auo_feature_enhance_model_b",
                        "auo_feature_enhance_model_c": "auo_feature_enhance_model_c",
                        "auo_faster_convergency_model": "auo_faster_convergency_model",
                        "auo_unrestricted_powerful_model": "auo_unrestricted_powerful_model",
                        "auo_cross_connection_model": "auo_cross_connection_model",
                        "auo_feature_reuse_model": "auo_feature_reuse_model",
                        "auo_lighten_efficient_model": "auo_lighten_efficient_model",
                        "auo_horizontal_sample_model": "auo_horizontal_sample_model"
                    }
                },
                "pretrained": {
                    "type": "boolean",
                    "default": True
                }
            },
            "ClsModelPara": {
                "batchSize": {
                    "type": "int",
                    "default": 1,
                    "min": 1,
                    "unit": "/batch"
                },
                "epochs": {
                    "type": "int",
                    "default": 1,
                    "min": 1,
                    "unit": "epochs"
                }
            }
        }
    },
    # "ConfigEvaluation": {
    #     "EvaluationPara": {
    #         "accuracy": {
    #             "mode": {
    #                 "type": "list",
    #                 "default": ['Train', 'Valid', 'Test'],
    #                 "options": ['Train', 'Valid', 'Test']
    #             },
    #             "saveTxt": {
    #                 "type": "boolean",
    #                 "default": True
    #             },
    #             "saveJson": {
    #                 "type": "boolean",
    #                 "default": True
    #             }
    #         },
    #         "accOfClasses": {
    #             "mode": {
    #                 "type": "list",
    #                 "default": ['Valid', 'Test'],
    #                 "options": ['Train', 'Valid', 'Test']
    #             },
    #             "saveTxt": {
    #                 "type": "boolean",
    #                 "default": True
    #             },
    #             "saveJson": {
    #                 "type": "boolean",
    #                 "default": True
    #             }
    #         },
    #         "numOfClasses": {
    #             "mode": {
    #                 "type": "list",
    #                 "default": ['Valid', 'Test'],
    #                 "options": ['Train', 'Valid', 'Test']
    #             },
    #             "saveTxt": {
    #                 "type": "boolean",
    #                 "default": True
    #             },
    #             "saveJson": {
    #                 "type": "boolean",
    #                 "default": True
    #             }
    #         },
    #         "otherClsRate": {
    #             "posClass": ['OK'],
    #             "negClass": ['NG'],
    #             "saveTxt": {
    #                 "type": "boolean",
    #                 "default": True
    #             },
    #             "saveJson": {
    #                 "type": "boolean",
    #                 "default": True
    #             }
    #         },
    #         "drawAccCurve": {
    #             "switch": True
    #         }
    #     }
    # },
    # "ConfigResultStorage": {
    #     "ResultStorage": {
    #         "saveFinalWeight": {
    #             "switch": {
    #                 "type": "boolean",
    #                 "default": False
    #             }
    #         },
    #         "saveAccTxt": {
    #             "switch": {
    #                 "type": "boolean",
    #                 "default": False
    #             }
    #         },
    #         "savePredictResult": {
    #             "switch": {
    #                 "type": "boolean",
    #                 "default": True
    #             }
    #         },
    #         "unknownFilter": {
    #             "switch": {
    #                 "type": "boolean",
    #                 "default": False
    #             },
    #             "filter": {
    #                 "type": "dict",
    #                 "children": {
    #                         "name": {
    #                             "type": "string",
    #                             "default": "unknown",
    #                         },
    #                     "threshold": {
    #                             "type": "float",
    #                             "default": 0.5,
    #                             "max": 1,
    #                             "min": 0
    #                         }
    #                 }
    #             },
    #             "reverse": {
    #                 "type": "boolean",
    #                 "default": False
    #             },
    #             "saveCsv": {
    #                 "type": "int",
    #                 "default": 2,
    #                 "enums": {
    #                         "unknownFilterNone": 0,
    #                         "unknownFilterFiltered": 1,
    #                         "unknownFilterAll": 2
    #                 }
    #             }
    #         }
    #     }
    # }
}
