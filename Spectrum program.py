# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 19:16:30 2016

@author: Caspar!
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 17:20:24 2016

@author: Caspar!
"""

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
om = [0.0] * 584 
omspec = [0.0] *584
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
   omspec[k] = abs(1.94e+14-freq[k])
     
   om[k] = om[k]/3e8
   om[k] = om[k]/100 

   k += 1
#print om

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

power = [0.0]*584
power[465] = 1.58e-3
power2 = [0.0]*584
power2[465] = 1.58e-3
Aeff = 1e-10


q=0
term1 = 0.0
term2 = 0.0 
term3 = 0.0
term4 = 0.0
leng = 0
gain = 0.0
while leng<2001:
 #print leng    
 q=0 
 while q<584:
    alphray = ((8*pow(math.pi,3))/(3*pow(wav[q],4)))*pow(1.46,8)*0.286*0.286*1.38e-23*7e-11*1950
    term1 = 0.0
    term2 = 0.0 
    term3 = 0.0
    term4 = 0.0
    if q<195:
        alpha = 0.0017372
    if 195<q<440:
        alpha = 0.004343
    if 440<q<485:
        alpha= 0.000868
    if 485<q:
        alpha = 0.0026058
    
    b = 0
    while b<q:
 
        abc = ((s[b]*(pow(10,1)))/Aeff)
        d = power[b]*100e9
        
        
        term1 += (abc) * (d)
        
        #if (abc*d)<0:
            #print freq[q]
            #print freq[b]
            #print power[b]
            #print abc
            #print d
            #print "break"
         
        term2 += ((s[b]*(pow(10,1)))/Aeff)*power[b]*100e9*6.63e-34*freq[q]*(1+(1/(math.exp((6.63e-34*(freq[b]-freq[q]))/(1.38e-23*298))-1)))
        
        b+=1
    b+=1
    while b<584:#IM GOING TO IGNORE GROUP VELOCITY FOR NOW
       
        term3 += ((s[b]*(pow(10,1)))/Aeff)*power[b]*100e9*(freq[q]/freq[b])
        
        
        z = math.exp((6.63e-34*(freq[q]-freq[b]))/(1.38e-23*298))
       
        if z == 1:
            term4 +=  ((s[b]*(pow(10,1)))/Aeff)*power[b]*100e9*6.63e-34*freq[q]
        else:
            term4 +=  ((s[b]*(pow(10,1)))/Aeff)*power[b]*100e9*6.63e-34*freq[q]*(1+(1/(math.exp((6.63e-34*(freq[q]-freq[b]))/(1.38e-23*298))-1)))
            
        b+=1
  
    #print term1
    #print power [q]
    #print power[q]*term1
    #print "break2"    
   
    power2[q] = (-alpha*power[q])+(alphray*power[q])+(power[q]*term1)+(2*term2)-(power[q]*term3)+(2*term4)
    if power2[q]<0:
        power2[q]= abs(power2[q])
    power2[465] =  1.58e-3
    #print "new break"
       
    #print power2[q]
    #power2[q] = (alphray*power[q])+(power[q]*term1)+(2*term2)-(power[q]*term3)+(2*term4)
    #print power[q]
   # print "new break"
    q+=1
 
 
 m=0
 while m<584:
     xyz = power2[m]
     power [m] = xyz
     m+=1
 #print "power swap"
 leng +=1000   


m = 0
f = open("test spectrum results.txt", "w")
while m<584:
    #print s[m]
    
    out1 = str(power2[m])
   
    
    f.write("%s\n" % (out1))
    m += 1

f.close()





