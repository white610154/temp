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
            }
        }
    },
    "ConfigModelService": {
        "LossFunctionPara": {
            "lossFunction": {
                "type": "string",
                "default": "CrossEntropyLoss",
                "enums": {
                    "CrossEntropyLoss": "CrossEntropyLoss"
                }
            }
        },
        "LearningRate": {
            "learningRate": {
                "type": "float",
                "default": 0.001,
                "min": 0.001,
                "max": 0.001
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
            }
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
                        "auo_unrestricted_powerful_model": "auo_unrestricted_powerful_model",
                        "auo_cross_connection_model": "auo_cross_connection_model"
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
                    "default": 16,
                    "min": 16,
                    "max": 16,
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
