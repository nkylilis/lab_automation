#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 21:39:56 2021

@author: nicolaskylilis
"""

def growth_rate(df_time,df_samples):
    #%% plot background corrected growth curves
    import pandas as pd
    import numpy as np
    from moving_average import movingaverage
    import os
    
    dirname = 'growth_rate_data_&_plots'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    # dict of well blanks('0') and samples replicates labes
    l_col = list(df_samples.columns)
    # remove Unnamed entries
    for sample in reversed(l_col):
        if 'Unnamed' in sample:
            l_col.remove(sample)
    
    d_repeats = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[]}
    for s in l_col:
        try:
            sample = s.split('.')[0]
            repeat = s.split('.')[1]
            d_repeats[repeat].append(s)
        except:
            d_repeats["0"].append(s)
    
    # correct for background absorbance in samples labels blank( .X)
    df_samples_bg_corr = pd.DataFrame([])
    
    count = 0
    for key in d_repeats:
        if key == "0":
            count += 1
            l_ = d_repeats[key]
            for item in l_:
                series_temp = pd.Series(data = df_samples[item].values - df_samples["blank"].values, name = str(item))
                df_samples_bg_corr.insert(len(df_samples_bg_corr.columns), series_temp.name, series_temp, allow_duplicates=False)
        else:
            l_ = d_repeats[key]
            for item in l_:
                series_temp = pd.Series(data = df_samples[item].values - df_samples["blank"+"." +str(count)].values, name = str(item))
                df_samples_bg_corr.insert(len(df_samples_bg_corr.columns), series_temp.name, series_temp, allow_duplicates=False)
            count += 1
    df_samples_bg_corr_time = pd.concat([df_time.to_frame(), df_samples_bg_corr], axis= 1)
    df_samples_bg_corr_time.set_index("Time", inplace = True)
    df_samples_bg_corr_time.to_csv(dirname + "/growth_curves_bg_corrected.csv", sep=',', header=True, index=True, index_label="Time")
    
    # growth rate section
    df_r = pd.DataFrame(df_time)
    for key in d_repeats.keys():
        for sample in d_repeats[key]:
            if "blank" in sample:
                pass
            else:
                # calculate growth rate
                b = np.log(df_samples_bg_corr[sample].to_frame())
                a = pd.concat([pd.DataFrame([np.nan]), b])[0:-1]
                r = (np.array(b[sample]) - np.array(a[sample]))/(df_time[1])
                df_r.insert(len(df_r.columns), sample, r, allow_duplicates=False)
    df_r.set_index("Time", inplace = True)
    df_r.to_csv(dirname + "/growth_rates.csv", sep=',', header=True, index=True, index_label="Time")
    
    
    #%% Plotting
    # plot backround corrected growth curves
    import os
    from matplotlib import pyplot as plt
        
    x = df_samples_bg_corr_time.index

    for col in l_col:
        y = df_samples_bg_corr[col]
        
        plt.plot(x,y)
        
        plt.xlabel('Time (minutes)')
        plt.ylabel('Absorbance_600nm (au)')
        plt.ylim(0,1)
        
        plt.savefig(dirname + '/growth_curves_bg_corr_' + str(col) + '.png')
        plt.close()
        
    # plotting growth rate curves
    x = list(df_r.index)
        
    l_col = list(df_r.columns)
    for col in l_col:
        y = df_r[col]
        y = movingaverage(y, 3)
        
        plt.plot(x[1:-1],y,'k')
        
        plt.xlabel('Time (minutes)')
        plt.ylabel('growth rate (h-1)')
        plt.title(col)
        
        plt.savefig(dirname + '/growth_rate_' + str(col) + '.png')
        plt.close()
        
    #%% Max growth rate
    df_max_r = df_r.max(axis=0, skipna=None).to_frame()
    df_max_r.rename(columns={0: "max_gowth_rate"}, inplace=True)
    df_max_r.to_csv(dirname + "/max_growth_rates.csv", sep=',', header=True, index=True, index_label="Sample")
