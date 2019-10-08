'''import serial
import os
from time import sleep
if __name__ == '__main__':
    serial = serial.Serial('/dev/ttyUSB1', 9600,timeout = 3600)
    if serial.isOpen() :
        print("open success")
    else :
        print("open failed")
    while True:
        data=serial.read(1)
        sleep(1)
        data = (data + serial.read(serial.inWaiting())).decode()
        print(data)'''



import serial
import pynmea2
import time
from time import sleep
import math

ser = serial.Serial("/dev/ttyUSB1",9600)

while True:
    line = ser.read(ser.inWaiting())
    line=line.decode()
    sleep(1)
    #line='$GPGGA,082516.000,4009.5087,N,11617.1488,E,1,6,1.46,-1.0,M,-6.7,M,,*63\r\n'
    l=line.splitlines(True)
    #print(line)
    for x in l:
        #print(x)
        if x.startswith('$GPGGA'):
            try:
                rmc = pynmea2.parse(x)
                Latitude=float(rmc.lat) / 100
                Longitude=float(rmc.lon)/100

                #sleep(0.1)
                #Latitude = floor(Latitude) + (Latitude - floor(Latitude)) * 100 / 60
                #Longitude = floor(Longitude) + (Longitude - floor(Longitude)) * 100 / 60
                Latitude=math.modf(Latitude)[1]+(math.modf(Latitude)[0] * 100 / 60)
                Longitude = math.modf(Longitude)[1] + (math.modf(Longitude)[0] * 100 / 60)

                print ("Latitude:  ")
                print (Latitude)
                print ("Longitude: ")
                print (Longitude)
                break
            except:
                pass