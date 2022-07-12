# -*- coding: utf-8 -*-

"""
Created on Jun Tue 14 22:00:00 2022
"""

from config.ConfigPostprocess import PostProcessPara
from .ConfidenceFilter import confidence_filter
from .UnknownFilter import unknown_filter

def select_postprocess(ResultList:list) -> None:
    """
    According to configs in ConfigPostprocess, select the post processing method.

    Args:
        ResultList: result list form model
    Return:
        ResultList: after post-processing
    """
    if PostProcessPara.confidenceFilter["switch"]:
        ResultList = confidence_filter(ResultList,
                                       PostProcessPara.confidenceFilter["threshold"])
    if PostProcessPara.unknownFilter["switch"]:
        ResultList = unknown_filter(ResultList,
                                    PostProcessPara.unknownFilter["threshold"],
                                    PostProcessPara.unknownFilter["reverse"])
    return ResultList