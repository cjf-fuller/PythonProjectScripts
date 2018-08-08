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
    threshold = [-0.22]
    delay = [1.25]
    
    n_samples = 10 #Set number of samples for each measurement
   
    lmin = 1450.00 #Set min. lambda 
    lmax = 1549.70 #set max. lambda
    step = 0.1 # set increment for lambda
    #lambdas = [lmin - (i*step) for i in xrange(int((lmin-lmax)/step)+1)]  
    lambdas = [lmin + (i*step) for i in xrange(int((lmax-lmin)/step)+1)]  
    
    
    filename = r'Lambda_Overnight.csv'
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
    
   
    write_str = 'Set Lambda Up(nm)'#set up file
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
    xta.write('LAMBDA = 1450.000') #set lmin 
    time.sleep(1)    
    xta.write('FWHM = 0.1') # set correct FWHM
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
    
    
    write_str = 'Set Lambda Dowm (nm)'#set up file
    for i in detector:
        write_str += ', Detector ' + str(i) +' (cts/s), Error Counts' 
        #write_str += ', Detector ' + str(i) 
    write_str += '\n'
    print write_str
    
    with open(filename, 'a') as f:
        f.write(write_str)
        
    lmin = 1549.60 #Set min. lambda 
    lmax = 1450.00 #set max. lambda
    step = 0.1 # set increment for lambda
    lambdas = [lmin - (i*step) for i in xrange(int((lmin-lmax)/step)+1)]  
         
    j=0
    xta.write('LAMBDA = 1549.60') #set lmin 
    time.sleep(1)    
    xta.write('FWHM = 0.1') # set correct FWHM
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
    
   