# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""

### Choose result storage method ###
class ResultStorage:
    saveFinalWeight = False                           # Save final weight
    saveCheckpoint  = {'switch': True, 'saveIter': 1} # Save checkpoint weight for every 'saveIter' epochs
    
    saveAccTxt      = True     # Save validation accuracy in txt file
    drawAccCurve    = True     # Save validation accuracy curve in jpg
    drawConfusionMatrix = True # Draw confusion matrix for test task
