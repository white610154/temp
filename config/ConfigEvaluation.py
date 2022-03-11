# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""

class EvaluationPara:
    showAcc          = True                                    # Show overall accuracy.
    showClassAcc     = True                                    # Show individual class accuracy.
    showNumOfClasses = False                                   # Show amount of total images and correctly predicted images.
    showRate         = {'switch': False, 'targetIndex': 'Pass'}   # Show overkill、leakage、defect accuracy.
    showWrongFile    = False                                   # Show file name of wrong predicted images.
