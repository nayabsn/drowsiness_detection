from serial import *
from lxml import *

ser = Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
    
while True:
    if ser.in_waiting > 0:
        
        #line = ser.readline().decode('utf-8').rstrip()
        b = ser.readline()
        string_n = b.decode()  # decode byte string into Unicode  
        string = string_n.rstrip() # remove \n and \r
        flt = float(string)        # convert string to float
        print("Pressure: " + str(flt))
