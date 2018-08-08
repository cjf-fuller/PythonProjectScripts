

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
    detector = [2] #set detectors up as usual here (MAKE SURE THIS SAYS 11)
    threshold = [-0.38]
    delay = [1.25]
    
    n_samples = 10 #Set number of samples for each measurement
   
    fmin = 0.05 #Set min. lambda 
    fmax = 0.95 #set max. lambda
    step = 0.025 # set increment for lambda
    fwhms = [fmin + (i*step) for i in xrange(int((fmax-fmin)/step)+1)]  
    
    
    filename = r'FWHM_SNSPD.csv'
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
    
   
    write_str = 'Set FWHM (nm)'#set up file
    for i in detector:
        write_str += ', Detector ' + str(i) +' (cts/s)'
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
    xta.write('LAMBDA = 1550.000') #set lmin 
    time.sleep(1)    
    xta.write('FWHM = 0.05') # set correct FWHM
    counts = [[] for i in detector]
    
    
    
    k = fwhms[j]
    while k != fmax:
        
        
        print(xta.write('FWHM =' + str(k) ))
        time.sleep(1.5)
        
        
        if len(detector) > 0:
            results = dc.get_results(n_samples)
            for it, val in enumerate(counts):
                val.append(np.mean(results.counts[it]))
        
        write_str = str(k)
        for i in counts:
            write_str += ', ' + str(i[j])
        write_str += '\n'
        
        print write_str
        with open(filename, 'a') as f:
            f.write(write_str)
        j += 1
        k = fwhms[j]
    
    '''
    Clean up
    '''
    xta.close()
    dc.close()
    
    '''
    Plot if you desire
    '''
    if plots:
        
        plt.figure()
        plt.xlabel('FWHM (nm)')
        plt.ylabel('Count Rate (cts/s)')
        for cts, det in zip(counts, detector):
            plt.plot(fwhms, cts, label = str(det))
        plt.legend()
        plt.show()