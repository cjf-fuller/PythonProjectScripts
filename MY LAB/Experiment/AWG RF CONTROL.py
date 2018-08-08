# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:09:49 2017

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
    detector = [5,6] #set detectors up as usual here (MAKE SURE THIS is correcct)
    threshold = [-0.1,-0.1]
    delay = [0,0]
    coincidence_window_ns= 2.0
    histogram_window_ns = 30.0
    
    n_samples = 10 #Set number of samples for each measurement
   
    pmin = -12.00
    pmax = -1.5
    step = 0.5
    powers = [pmin + (i*step) for i in xrange(int((pmax-pmin)/step)+1)]  
    
    
    filename = r'power-extinction.csv'
    
    
    '''
    End of parameters setup
    '''
    
    '''
    Initialise kit
    '''    
    ''    
    rm = visa.ResourceManager()
    awg = rm.open_resource('USB0::0x0957::0x5B18::IL50280105::INSTR') #connect filter
    
    
    if len(detector) > 0: #connect detector
        dc = DetectorConnection()
        dc.set_poll_time(15)        
        dc.add_channels(detector, threshold, delay)
        dc.add_coincidence(detector, coincidence_window_ns)
        dc.add_histogram(detector, histogram_window_ns)
    
    coincidence = []
    histogram = []
    data = ' '
   
   
    write_str = 'Power (dBm)'#set up file
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
    
    awg.write(':INST:SEL CH1')
    awg.write(':OUTP:COUP AC')
    awg.write(':SOUR:FUNC:SHAP SIN')
    awg.write(':SOUR:FREQ:CW 50e6') #SET FREQ OF OCILLATION (OPTIMIZE FOR HISTOGRAM SPACE)
    awg.write(':SOUR:POW:LEV:AMPL -11')
    awg.write('OUTP:STAT ON')
    counts = [[] for i in detector]
  
    
    b=0
    k = powers[b]
    while k != pmax:
        
        
        print(awg.write(':OUR:POW:LEV:AMPL ' + str(k) ))
        
        
        
        if len(detector) > 0:
            results = dc.get_results(n_samples)
            coincidence.append(np.mean(coincidence))
            histogram.append([sum(i) for i in results.histogram_counts])
            err = [np.sqrt(i) for i in histogram[len(histogram)-1]]
            data = str(k)
            for i in results.histogram_counts:
                     print i
            for i,m in zip(histogram, err):
               for j in i:
                data += ', ' + str(j) + ', ' + str(m) + '\n'
            with open(filename, 'a') as f:
                f.write(data)
            plots = True
            if plots:
                          
              plt.figure()
              #err = [np.sqrt(i) for i in histogram[len(histogram)-1]]
              plt.bar(np.linspace(0,int(histogram_window_ns), len(histogram[len(histogram)-1])), histogram[len(histogram)-1], yerr = err)
              plt.xlabel("Delay (ns)")
              plt.ylabel("Coincidences")
              title_str = "new pulse Coincidence at Power:" + str(k) 
              plt.title(title_str)
              plt.savefig(title_str + str(k) + '.png')
             
        
      
        b += 1
        k = powers[b]
    
    '''
    Clean up
    '''
    awg.write('OUTP:STAT OFF')
    awg.close()
    dc.close()
 