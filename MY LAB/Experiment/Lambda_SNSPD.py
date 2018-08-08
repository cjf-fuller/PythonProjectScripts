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
    
    n_samples = 10 #Set number of samples for each measurement
   
    lmin = 1570.3 #set min. lambda 
    lmax = 1550.9 #set max. lambda
    step = 0.2 # set increment for lambda
    lambdas = [lmin - (i*step) for i in xrange(int((lmin-lmax)/step)+1)]  
    #lambdas = [lmin + (i*step) for i in xrange(int((lmax-lmin)/step)+1)]  
    
    
    filename = r'Lambda_SNSPD.csv'
    plots = True
    
    '''
    End of parameters setup
    '''
    
    '''
    Initialise kit
    '''    
    ''    
    rm = visa.ResourceManager()

    xta = rm.open_resource('TCPIP::192.168.54.1::5025::SOCKET') #connect filter
    xta.term_chars = "\n"
    
    if len(detector) > 0: #connect detector
        dc = DetectorConnection()
        dc.add_channels(detector, threshold, delay)
    
   
    write_str = 'Set Lambda (nm)'#set up file
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
    
    j=0
    xta.write('LAMBDA = 1570.3') #set lmin 
    time.sleep(1)    
    xta.write('FWHM = 0.05') # set correct FWHM
    counts = [[] for i in detector]
    count_sd = []
    
    
    k = lambdas[j]
    while k != lmax:
        
        
        print(xta.write('LAMBDA =' + str(k) ))
        time.sleep(1.5)
        
        
        if len(detector) > 0:
            results = dc.get_results(n_samples)
            for it, val in enumerate(counts):
                val.append(np.mean(results.counts[it]))
                count_sd.append(np.std(results.counts[it]))
        
        write_str = str(k)
        for i in counts:
            write_str += ', ' + str(i[j]) + ', ' + str(count_sd[j])
            #write_str += ', ' + str(i[j]) 
        write_str += '\n'
        
        print write_str
        with open(filename, 'a') as f:
            f.write(write_str)
        j += 1
        k = lambdas[j]
    
    '''
    Clean up
    '''
    xta.close()
    dc.close()
    
   