class PostProcessPara:
    confidenceFilter = {"switch": False, "threshold": {}}
    unknownFilter = {"switch": True, "threshold": {"Unknown": 0.99}, "reverse": False, "saveCsvMode": 0}