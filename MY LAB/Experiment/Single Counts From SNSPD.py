# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 15:03:53 2017

@author: Caspar!
"""

from __future__ import division
import __init__
import numpy as np
import matplotlib.pyplot as plt
import visa
import time
from detectorconnection import DetectorConnection

if __name__ == '__main__':
    
    '''
    Setup Parameters
    '''
    detector = [5] #set detectors up as usual here (MAKE SURE THIS is correcct)
    threshold = [-0.08]
    delay = [1.25]
    
    n_samples = 15#Set number of samples for each measurement
   
    filename = r'counter_results.csv'
    plots = True
    
    '''

    End of parameters setup
    '''
    
    '''
    Initialise kit
    '''    
    
    if len(detector) > 0: #connect detector
        dc = DetectorConnection()
        dc.add_channels(detector, threshold, delay)
    
   
    write_str = 'Distance'#set up file
    for i in detector:
        write_str += ', Detector ' + str(i) +' (cts/s), Error Counts' 
        #write_str += ', Detector ' + str(i) 
    write_str += '\n'
    print write_str
    
    with open(filename, 'w') as f:
        f.write(write_str)
        
    '''
    End of initialisation 
    '''    
    
    '''
    Do measurement
    '''
    #Turn on output, but make sure it is 0
    
    
    counts = [[] for i in detector]
    count_sd = []
    j = 0 
        
    if len(detector) > 0:
            results = dc.get_results(n_samples)
            for it, val in enumerate(counts):
                val.append(np.mean(results.counts[it]))
                count_sd.append(np.std(results.counts[it]))
        
    write_str = 'DC '
    for i in counts:
            write_str += ', ' + str(i[j]) + ', ' + str(count_sd[j])
            #write_str += ', ' + str(i[j]) 
    write_str += '\n'
        
    print write_str
    with open(filename, 'a') as f:
            f.write(write_str)    
    '''
    Clean up
    '''
  
    dc.close()
    