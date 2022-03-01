# -*- coding: utf-8 -*-

"""
Created on Mon Feb 7 11:00:00 2022
@author: OtisChang
"""
from config.Config import PrivateSetting

class PostProcessPara:
    confidenceFilter = {'switch': True, 
                        'threshold': 0.8, 
                        'selectLabel': 'OK', 
                        'classList': ['AU02', 'EN01', 'EN02', 'EN03', 'IT43', 
                                     'OK', 'SM00.OT08', 'SM03.SM07', 'SM04', 'SM05']
                       }
