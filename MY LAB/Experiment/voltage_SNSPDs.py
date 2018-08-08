

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 15:03:53 2017

@author: Caspar!
"""

from __future__ import division
import numpy as np
from detectorconnection import DetectorConnection
import time
if __name__ == '__main__':
    
    '''
    Setup Parameters
    '''
    detector = [5] #set detectors up as usual here (MAKE SURE THIS is correcct)
    threshold = [-0.1]
    delay = [0]
    
    n_samples = 10 #Set number of samples for each measurement
   
    
    
    filename = r'Voltage-Counts_SNSPD.csv'
    
    '''
    End of parameters setup
    '''
    
    '''
    Initialise kit
    '''    
    ''    
 
    if len(detector) > 0: #connect detector
        dc = DetectorConnection()
        dc.add_channels(detector, threshold, delay)
    
   
    write_str = 'Voltage (V)'#set up file
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

    counts = [[] for i in detector]
    count_sd = []
    
    
    j=0
    while j != 9999:
        
        write_str =  raw_input('Enter Voltage (or end to finish): ')
        if write_str == 'end':
            break              
        results = dc.get_results(n_samples)
        #print results
        for it, val in enumerate(counts):
                val.append(np.mean(results.counts[it]))
                count_sd.append(np.std(results.counts[it]))
        
        for i in counts:
             write_str += ', ' + str(i[j]) + ', ' + str(count_sd[j])
             
        write_str += '\n'
        print write_str
        with open(filename, 'a') as f:
             f.write(write_str)
        j += 1
        print 'Change Voltage Now'
        cont = raw_input('Press Enter When Ready')
    '''
    Clean up
    '''
   
    dc.close()
    
   