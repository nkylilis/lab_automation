#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 10:51:23 2021

@author: nicolaskylilis
"""

#%% User manual
""" 
1) Enter the filename that incledes the raw data from plate reader here:
"""

"""Plate reader raw data """
data = "example_data.csv"
 
"""
2) Structure of raw data file:
    
col index    Time    blank   Sample_1    Sample _2     blank      Sample_1    Sample _2  (empty well - no label)
    1          0        0.1      0.15       0.15          0.1       0.15         0.15         0
    2         10        0.1      0.15       0.15          0.1       0.15         0.15         0
    3         20        0.1      0.15       0.15          0.1       0.15         0.15         0
    .          .          .        .           .            .          .           .          .
    .          .          .        .           .            .          .           .          .
    .          .          .        .           .            .          .           .          .
   96        950        0.1      0.15       0.15          0.1       0.15         0.15         0

Note 1: Time is in minutes
Note 2: Replicates must have the same label
Note 3: Media blank must be labelled as blank
Note 4: Wells with no sample added should be left without any label on top raw

"""

"""Switches"""
# activate/deactivate growth curves plotting function by switch = 1/0
switch_od = 1
# activate/deactivate growth rate function by switch = 1/0
switch_gr = 1

#%% Load data

import pandas as pd

df = pd.read_csv(data, sep = ',')
"""
# convert time to float minutes
timeseries = df.Time
new_time = []
for t in timeseries:
    l_time = t.split(':')
    l_time_int = [float(item) for item in l_time]
    time =  (l_time_int[0] * 60) + l_time_int[1] + (l_time_int[2]/60)
    new_time += [time]
df.Time = new_time
"""
df_time = df.Time                                                                                                                        
#df_time.dropna(inplace=True)

df_samples = df.drop("Time", axis = 1)

#%% Section:
#       *  plots growth curves

# packages and modules
from growth_curves import growth_curves

# function
if switch_od == 1:
    growth_curves(df_time,df_samples)


#%% Section:
#       * plots growth rate curves
#       * calculates max growth rate for each sample
#       * plots background corrected growth curves

# packages and modules
from growth_rate import growth_rate

# function
if switch_gr == 1:
    growth_rate(df_time,df_samples)

