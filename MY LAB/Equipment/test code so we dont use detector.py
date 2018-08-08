# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 15:24:39 2017

@author: Caspar!
"""
import visa
import time

rm = visa.ResourceManager()

xta = rm.open_resource('TCPIP::192.168.54.1::5025::SOCKET')
xta.term_chars = "\n"
j=0
lmin = 1530.000 #Set min. lambda 
lmax = 1549.000 #set max. lambda
step = 0.2 # set increment for lambda
lambdas = [lmin + (i*step) for i in xrange(int((lmax-lmin)/step)+1)]  
k = lambdas[j]
while k != lmax:
        
        
        print(xta.write('LAMBDA =' + str(k) ))
        time.sleep(0.5)
        j += 1
        k = lambdas[j]
xta.close()