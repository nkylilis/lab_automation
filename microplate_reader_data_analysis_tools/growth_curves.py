#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 12:44:14 2021

@author: nicolaskylilis
"""


def growth_curves(df_time, df_samples):
    
    
    
    import os
    from matplotlib import pyplot as plt
    
    dirname = 'growth_curves_plots'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
    x = df_time
    
    l_col = list(df_samples.columns)
    for col in l_col:
        if 'Unnamed' in col:
            pass
        else:
            y = df_samples[col]
            
            plt.plot(x,y,'k')
            
            plt.xlabel('Time (minutes)')
            plt.ylabel('Absorbance_600nm (au)')
            plt.ylim(0,1)
            plt.title(col)
            
            plt.savefig(dirname + '/growth_curve_' + str(col) + '.png')
            plt.close()
        
    print('Process upadate: Finshed plotting growth curves')
