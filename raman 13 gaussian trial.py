# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 15:36:45 2016

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
om = [0.0] * 2829 

s = [0.0] * 2829


om[0] = 0.0 


om[2828] = 1500.30059687953 

k = 1
while k<2828:
    
    om[k] = (om[k-1]+0.530516476972985)
    k += 1

j = 0
while j<2829:
    om[j] = 2*pi*om[j]
    
    j += 1
i=0
#c = 1
print om

while i<13:
    
    omv = 2*pi*CPs[i]
    hang = pi*Gs[i]
    gamma = pi*Ls[i]
    Adash = omv*Ais[i]
    
   
    l = 0
    while l<2829:
    
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
f = open("raman results.txt", "w")
while m<2829:
    #print s[m]
    
    out1 = str(s[m])
    out2 = str((om[m]/(2*pi)))
    
    f.write("%s\t %s\n" % (out2, out1))
    m += 1

f.close()
