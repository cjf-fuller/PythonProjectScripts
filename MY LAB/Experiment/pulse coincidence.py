# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:33:36 2017

@author: Caspar!
"""

from __future__ import division
import numpy as np
from detectorconnection import DetectorConnection
import matplotlib.pyplot as plt
if __name__ == '__main__':
    
    
    
    detector = [5,6] #set detectors up as usual here (MAKE SURE THIS is correcct)
    threshold = [-0.1,-0.1]
    delay = [0,0]
    coincidence_window_ns = 2.0
    histogram_window_ns = 30.0
    
    n_samples = 1 #Set number of samples for each measurement
   
    
    
    filename = r'Coincidence-Counts_SNSPD.csv'
    
    '''
    End of parameters setup
    '''
    
    '''
    Initialise kit
    '''    
    ''    
 
    if len(detector) > 0: #connect detector
        dc = DetectorConnection()
        dc.set_poll_time(30)
        dc.add_channels(detector, threshold, delay)
        dc.add_coincidence(detector, coincidence_window_ns)
        dc.add_histogram(detector, histogram_window_ns)
        
        
    coincidence = []
    histogram = []
    data = ' '
   
    write_str = 'Data 1'#set up file
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
    #count_sd = []
    
    if len(detector) > 0:
        results = dc.get_results(n_samples)
        coincidence.append(np.mean(coincidence))
       
        histogram.append([sum(i) for i in results.histogram_counts])
        err = [np.sqrt(i) for i in histogram[len(histogram)-1]]
        
        for i in results.histogram_counts:
            print i
        for i,k in zip(histogram, err):
            for j in i:
                data += str(j) + ', ' + str(k) + '\n'
        with open(filename, 'a') as f:
            f.write(data)
        plots = True
        if plots:
            plt.figure()
            #err = [np.sqrt(i) for i in histogram[len(histogram)-1]]
            plt.bar(np.linspace(0,int(histogram_window_ns), len(histogram[len(histogram)-1])), histogram[len(histogram)-1], yerr = err)
            plt.xlabel("Delay (ns)")
            plt.ylabel("Coincidences")
            title_str = "Pulse Coincidence"
            plt.title(title_str)
            plt.savefig("pulse coincidence plot good pulse")
  
    dc.close()
    
   