#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 15:38:17 2021

@author: nicolaskylilis
"""

def movingaverage (values, window):
    import numpy as np
    
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma