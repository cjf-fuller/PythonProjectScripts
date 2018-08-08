# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 17:20:24 2016

@author: Caspar!
"""

import math
import numpy 
from scipy import integrate as integrate

pi = math.pi


#Set up the value tables for the summation bit
CPs = [56.25, 100, 231.25, 362.50, 463.00, 497.00, 611.50, 691.67, 793.67, 835.50, 930.00, 1080.00, 1215.00]
Ais = [1.00, 11.40, 36.67, 67.67, 74.00, 4.50, 6.80, 4.60, 4.20, 4.50, 2.70, 3.10, 3.00]
Gs = [52.10, 110.42, 175.00, 162.50, 135.33, 24.50, 41.50, 155.00, 59.50, 64.30, 150.00, 91.00, 160.00]
Ls = [17.37, 38.81, 58.33, 54.17, 45.11, 8.17, 13.83, 51.67, 19.83, 21.43, 50.00, 30.33, 53.33]

#Set up the lists, one for omega values, one for s(omega)
om = [0.0] * 584 
wav = [0.0] * 584
freq = [0.0] * 584
s = [0.0] * 584


wav[0] = 1250e-9
freq [0] = 2.4e+14

k = 1
while k<584:
    
    wav[k] = wav[k-1] + 3e8*((1/(freq[k-1]-100e+9))-(1/freq[k-1]))
    freq [k] = 3e+8/(wav[k])
    k += 1

k = 0

while k<584:
   
      
   om[k] = 2*pi*abs(1.94e+14-freq[k])
   
     
   om[k] = om[k]/3e8
   om[k] = om[k]/100 

   k += 1
print om

i=0
#c = 1


while i<13:
    
    omv = 2*pi*CPs[i]
    hang = pi*Gs[i]
    gamma = pi*Ls[i]
    Adash = omv*Ais[i]
    
   
    l = 0
    while l<584:
    
      x = om[l]
      def f(t):
       cosbit = (math.cos((omv-x)*t)-math.cos((omv+x)*t))
       gamexp = math.exp(-gamma*t)
       hangexp = math.exp(-math.pow((hang*t),2)/4)
       return cosbit*gamexp*hangexp
      result = integrate.quad(f,0,numpy.inf, limit=200)
      
      s[l] += result[0] * (Adash/(2*omv))
      l += 1
    i += 1
    print "new i"
m = 0
f = open("NEW wavelength results.txt", "w")
while m<584:
    #print s[m]
    
    out1 = str(s[m])
    out2 = str((om[m]/(2*pi)))
    
    f.write("%s\t %s\n" % (out2, out1))
    m += 1

f.close()
