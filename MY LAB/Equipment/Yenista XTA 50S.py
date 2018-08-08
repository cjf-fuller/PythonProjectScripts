# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 17:57:12 2017

@author: Caspar!
"""


from __future__ import division
import __init__
import visa
import time



class yenista_xta50(object):
    
    def __init__(self):
        self.rn = 0
        self.rm = visa.ResourceManager()
        self.inst = 0
        self.buffername = "\"vbuf\""
        self.output = False
        
    def connect(self, resourceName = 'TCPIP::192.168.54.1::5025::SOCKET'): #Connection via ethernet. 
        self.rn = resourceName
        self.reset()
        
    def reset(self):
        self.inst = self.rm.open_resource(self.rn)
        self.inst.write("FWHM = 0.05")
        time.sleep(1)
        
    def setLambda(self, w):
       
        self.inst.write("LAMBDA =" + str(w))
        time.sleep(1)
        
    def setFWHM(self, f):
        self.inst.write("FWHM = " + str(f))
        time.sleep(1)
    
    def setFreq(self, v):
        self.inst.write("FREQ = " + str(v))
        time.sleep(1)
        
    def setFWHM_F(self, fv):
        self.inst.write("FWHM_F =" + str(fv))
        time.sleep(1)

    def shutdown(self):
        self.rm.close
            
if __name__ == '__main__':
    xta = yenista_xta50()
    
    xta.connect()
   
    xta.setLambda(1546.6)
    xta.setFWHM(0.5)
    

    xta.shutdown()


