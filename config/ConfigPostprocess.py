# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""

class PostProcessPara:
    ### confidenceFilter: if the confidence of 'selectLabel' is lower than 'threshold', reduce the confidence to 0.
    confidenceFilter = {'switch': True, 
                        'threshold': 0.8, 
                        'selectLabel': 'Pass', 
                        # 'classList': ['AU02', 'EN01', 'EN02', 'EN03', 'IT43', 
                        #              'OK', 'SM00.OT08', 'SM03.SM07', 'SM04', 'SM05'],
                        'classList': ['Copper', 'Dimple', 'Nick', 'Open', 'Pass', 
                                     'Protrusion', 'Short']
                       }
