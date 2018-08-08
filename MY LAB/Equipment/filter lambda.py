import visa
import time

rm = visa.ResourceManager()

xta = rm.open_resource('TCPIP::192.168.54.1::5025::SOCKET')
xta.term_chars = "\n"
i=0
while i<200:
    
     j = 1450 + i
     print(xta.write('LAMBDA =' + str(j) ))
     time.sleep(0.5)
     print('hello')
     i += 10
xta.close()
    
