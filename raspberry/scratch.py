# !/usr/local/bin/python
# -*- coding:utf-8 -*-

import serial
import os
import time
import datetime
from time import sleep
import pynmea2
import binascii
import json
import RPi.GPIO as GPIO
import math

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(36, GPIO.OUT)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(38, GPIO.OUT)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT)

    ser = serial.Serial("/dev/ttyUSB1", 9600)
    serial = serial.Serial('/dev/ttyUSB0', 9600,timeout = 3600)
    #serial = serial.Serial('COM9', 9600, timeout=3600)
    if serial.isOpen() :
        print("open success")
    else :
        print("open failed")
    #while True:
    #send_data = input("input a data: ")
    data_judge='0'
    while data_judge!=b'\r\nOK\r\n':
        send_data='AT'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\nOK\r\n':
        send_data='AT+CMEE=1'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\nQuectel\r\n\r\nOK\r\n':
        send_data='AT+CGMI'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\nBC95HB-02-STD_900\r\n\r\nOK\r\n':
        send_data='AT+CGMM'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\nSECURITY,V100R100C10B657SP3\r\n\r\nPROTOCOL,V100R100C10B657SP3\r\n\r\nAPPLICATION,V100R100C10B657SP3\r\n\r\nSEC_UPDATER,V100R100C10B657SP3\r\n\r\nAPP_UPDATER,V100R100C10B657SP3\r\n\r\nRADIO,BC95HB-02-STD_900\r\n\r\nOK\r\n':
        send_data='AT+CGMR'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\n+NBAND:8\r\n\r\nOK\r\n':
        send_data='AT+NBAND?'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\n+NCONFIG:AUTOCONNECT,TRUE\r\n+NCONFIG:CR_0354_0338_SCRAMBLING,TRUE\r\n+NCONFIG:CR_0859_SI_AVOID,TRUE\r\n+NCONFIG:COMBINE_ATTACH,FALSE\r\n+NCONFIG:CELL_RESELECTION,FALSE\r\n+NCONFIG:ENABLE_BIP,FALSE\r\n\r\nOK\r\n':
        send_data='AT+NCONFIG?'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\n+CGSN:869405035846048\r\n\r\nOK\r\n':
        send_data='AT+CGSN=1'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\nOK\r\n':
        send_data='AT+CFUN=1'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\n460043193006443\r\n\r\nOK\r\n':
        send_data='AT+CIMI'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\nOK\r\n':
        send_data = 'AT+CGATT=0'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data = serial.read(1)
        sleep(0.5)
        data_judge = data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\n+CGATT:0\r\n\r\nOK\r\n':
        send_data = 'AT+CGATT?'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data = serial.read(1)
        sleep(0.5)
        data_judge = data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\nOK\r\n':
        send_data='AT+CGATT=1'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\n+CGATT:1\r\n\r\nOK\r\n':
        send_data='AT+CGATT?'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge=b'\r\n+CSQ:99,99\r\n\r\nOK\r\n'
    while data_judge==b'\r\n+CSQ:99,99\r\n\r\nOK\r\n':
        send_data='AT+CSQ'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\n+COPS:0,2,"46000"\r\n\r\nOK\r\n':
        send_data='AT+COPS?'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    data_judge='0'
    while data_judge!=b'\r\n+CEREG:0,1\r\n\r\nOK\r\n':
        send_data='AT+CEREG?'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)

    line = ser.read(ser.inWaiting())
    line = line.decode()

    send_data='AT+NUESTATS'
    print(send_data)
    send_data = send_data + '\r\n'
    serial.write(send_data.encode())
    data=serial.read(1)
    sleep(0.5)
    data_judge=data + serial.read(serial.inWaiting())
    print(data_judge)
    data_judge='0'



    #测试服务器是否可用
    '''while data_judge!=b'\r\nOK\r\n\r\n+NPING:139.199.105.136':
        send_data='AT+NPING=139.199.105.136'
        print(send_data)
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(5)
        data_judge=data + serial.read(serial.inWaiting())
        print(data_judge)   
        data_judge=data_judge[0:30]
        print(data_judge)'''

    try:
        #while True:
        while True:
            data_judge = '0'
            # sleep(1)
            while data_judge != b'\r\n0\r\n\r\nOK\r\n':
                send_data = 'AT+NSOCR=DGRAM,17,25535,1'
                print(send_data)
                send_data = send_data + '\r\n'
                serial.write(send_data.encode())
                data = serial.read(1)
                sleep(0.5)
                data_judge = data + serial.read(serial.inWaiting())
                print(data_judge)

            line = line.splitlines(True)

            for x in line:
                print(x)
                if x.startswith('$GPGGA'):
                    try:
                        '''rmc = pynmea2.parse(x)
                        legal = 'OK'
                        data = {'order':'ask','latitude': float(rmc.lat) / 100, "longitude": float(rmc.lon) / 100}
                        #data = {'order':'ask','latitude': 39.577238, "longitude": 116.21013}
                        data = json.dumps(data)
                        l = len(data)
                        judge = '0'
                        while judge != legal:
                            send_data = "AT+NSOST=0,139.199.105.136,25535," + str(len(data)) + "," + (
                                binascii.b2a_hex(str(data).encode('utf-8'))).decode()
                            print(send_data)
                            send_data = send_data + '\r\n'
                            serial.write(send_data.encode())
                            data = serial.read(1)
                            line = ser.read(ser.inWaiting())
                            line = line.decode()
                            sleep(1)
                            line = line.splitlines(True)
                            data = data + serial.read(serial.inWaiting())
                            data = str(data).split("\\r\\n")
                            print(data)
                            judge = data[3]
                        # print("Latitude:  ")
                        # print(float(rmc.lat) / 100)
                        # print("Longitude: ")
                        # print(float(rmc.lon) / 100)
                        # sleep(0.1)

                        if len(data) > 5:
                            # print(len(data))
                            # print(data[25:28])

                            # l=data[25:len(data)]
                            # data = str(data).split("\\r\\n")
                            print("进入判断")
                            data = data[5]
                            l = data[10:len(data)]

                            print(l)
                            data_judge = '0'
                            while data_judge != b'\r\n\r\nOK\r\n':
                                print("发送请求")
                                send_data = 'AT+NSORF=0,' + l + "\r\n"
                                print(send_data)
                                # send_data = send_data + '\r\n'
                                serial.write(send_data.encode())
                                data = serial.read(1)
                                sleep(1)
                                data = data + serial.read(serial.inWaiting())
                                # print(data.decode('utf-8'))
                                data_judge = data[len(data) - 8:len(data)]
                                data = str(data).split(",")
                                # print((bytearray.fromhex(data[4])).decode('utf-8'))
                                data = (bytearray.fromhex(data[4])).decode('utf-8')
                                data = json.loads(data)
                                print("receive:")
                                print(data)
                                if data['box_state'][0] == "open":
                                    GPIO.output(36, False)
                                    print("1号open")
                                if data['box_state'][0] == "close":
                                    GPIO.output(36, True)
                                    print("1号close")
                                if data['box_state'][1] == "open":
                                    GPIO.output(38, False)
                                    print("2号open")
                                if data['box_state'][1] == "close":
                                    GPIO.output(38, True)
                                    print("2号close")
                                if data['box_state'][2] == "open":
                                    GPIO.output(40, False)
                                    print("3号open")
                                if data['box_state'][2] == "close":
                                    GPIO.output(40, True)
                                    print("3号close")
                                if data['box_state'][2] == "open" and data['box_state'][1] == "open" and \
                                                data['box_state'][0] == "open" and data['car_state'] == 'c':
                                    print("转换为行进过程")

                                    judge = '0'
                                    data = {'order': 'car_state'}
                                    data = json.dumps(data)
                                    l = len(data)
                                    legal = "\r\n0," + str(len(data)) + "\r\n\r\nOK\r\n"

                                    while judge != legal.encode('utf-8'):
                                        send_data = "AT+NSOST=0,139.199.105.136,25535," + str(len(data)) + "," + (
                                            binascii.b2a_hex(str(data).encode('utf-8'))).decode()
                                        print(send_data)
                                        send_data = send_data + '\r\n'
                                        serial.write(send_data.encode())
                                        data = serial.read(1)
                                        sleep(1)
                                        data = data + serial.read(serial.inWaiting())
                                        print(data)
                                        judge = data[0:14]
                                        # print(judge)
                                        # print(legal)
                                        # data=data[13:len(data)]

                                    if len(data) > 13:
                                        print(len(data))
                                        # print(data[25:28])
                                        data_judge = '0'
                                        # l=data[25:len(data)]
                                        data = str(data).split("\\r\\n")
                                        data = data[5]
                                        l = data[10:len(data)]
                                        while data_judge != b'\r\n\r\nOK\r\n':
                                            send_data = 'AT+NSORF=0,' + l + "\r\n"
                                            print(send_data)
                                            # send_data = send_data + '\r\n'
                                            serial.write(send_data.encode())
                                            data = serial.read(1)
                                            sleep(0.5)
                                            data = data + serial.read(serial.inWaiting())
                                            # print(data.decode('utf-8'))
                                            data_judge = data[len(data) - 8:len(data)]
                                            data = str(data).split(",")
                                            # print((bytearray.fromhex(data[4])).decode('utf-8'))
                                            data = (bytearray.fromhex(data[4])).decode('utf-8')
                                            data = json.loads(data)
                                            print("receive:")
                                            print(data)'''
                        rmc = pynmea2.parse(x)
                        Latitude=float(rmc.lat) / 100
                        Longitude=float(rmc.lon)/100
                        Latitude = math.modf(Latitude)[1] + (math.modf(Latitude)[0] * 100 / 60)
                        Longitude = math.modf(Longitude)[1] + (math.modf(Longitude)[0] * 100 / 60)
                        print("Latitude:  ")
                        print(Latitude)
                        print("Longitude: ")
                        print(Longitude)

                        legal = 'OK'
                        if Longitude<116 or Latitude<39:
                            data = {'order': 'ask'}
                        else:
                            data = {'order': 'ask', 'latitude': Latitude, "longitude": Longitude}
                        data = json.dumps(data)
                        l = len(data)
                        judge = '0'
                        while judge != legal:
                            send_data = "AT+NSOST=0,139.199.105.136,25535," + str(len(data)) + "," + (
                                binascii.b2a_hex(str(data).encode('utf-8'))).decode()
                            print(send_data)
                            send_data = send_data + '\r\n'
                            serial.write(send_data.encode())
                            data = serial.read(1)
                            line = ser.read(ser.inWaiting())
                            line = line.decode()
                            sleep(2)
                            line = line.splitlines(True)
                            data = data + serial.read(serial.inWaiting())
                            data = str(data).split("\\r\\n")
                            print(data)
                            judge = data[3]

                        # print("Latitude:  ")
                        # print(float(rmc.lat) / 100)
                        # print("Longitude: ")
                        # print(float(rmc.lon) / 100)
                        # sleep(0.1)

                        if len(data) > 5:
                            # print(len(data))
                            # print(data[25:28])

                            # l=data[25:len(data)]
                            # data = str(data).split("\\r\\n")
                            print("进入判断")
                            data = data[5]
                            l = data[10:len(data)]

                            print(l)
                            data_judge = '0'
                            while data_judge != b'\r\n\r\nOK\r\n':
                                print("发送请求")
                                send_data = 'AT+NSORF=0,' + l + "\r\n"
                                print(send_data)
                                # send_data = send_data + '\r\n'
                                serial.write(send_data.encode())
                                data = serial.read(1)
                                sleep(1)
                                data = data + serial.read(serial.inWaiting())
                                # print(data.decode('utf-8'))
                                data_judge = data[len(data) - 8:len(data)]
                                data = str(data).split(",")
                                # print((bytearray.fromhex(data[4])).decode('utf-8'))
                                data = (bytearray.fromhex(data[4])).decode('utf-8')
                                data = json.loads(data)
                                print("receive:")
                                print(data)
                                if data['box_state'][0] == "open":
                                    GPIO.output(36, False)
                                    print("1号open")
                                if data['box_state'][0] == "close":
                                    GPIO.output(36, True)
                                    print("1号close")
                                if data['box_state'][1] == "open":
                                    GPIO.output(38, False)
                                    print("2号open")
                                if data['box_state'][1] == "close":
                                    GPIO.output(38, True)
                                    print("2号close")
                                if data['box_state'][2] == "open":
                                    GPIO.output(40, False)
                                    print("3号open")
                                if data['box_state'][2] == "close":
                                    GPIO.output(40, True)
                                    print("3号close")
                                if data['box_state'][2] == "open" and data['box_state'][1] == "open" and \
                                                data['box_state'][0] == "open" and data['car_state'] == 'c':
                                    print("转换为行进过程")

                                    judge = '0'
                                    data = {'order': 'car_state'}
                                    data = json.dumps(data)
                                    l = len(data)
                                    legal = "\r\n0," + str(len(data)) + "\r\n\r\nOK\r\n"

                                    while judge != legal.encode('utf-8'):
                                        send_data = "AT+NSOST=0,139.199.105.136,25535," + str(len(data)) + "," + (
                                            binascii.b2a_hex(str(data).encode('utf-8'))).decode()
                                        print(send_data)
                                        send_data = send_data + '\r\n'
                                        serial.write(send_data.encode())
                                        data = serial.read(1)
                                        sleep(2)
                                        data = data + serial.read(serial.inWaiting())
                                        print(data)
                                        judge = data[0:14]
                                        # print(judge)
                                        # print(legal)
                                        # data=data[13:len(data)]

                                    if len(data) > 13:
                                        print(len(data))
                                        # print(data[25:28])
                                        data_judge = '0'
                                        # l=data[25:len(data)]
                                        data = str(data).split("\\r\\n")
                                        data = data[5]
                                        l = data[10:len(data)]
                                        while data_judge != b'\r\n\r\nOK\r\n':
                                            send_data = 'AT+NSORF=0,' + l + "\r\n"
                                            print(send_data)
                                            # send_data = send_data + '\r\n'
                                            serial.write(send_data.encode())
                                            data = serial.read(1)
                                            sleep(0.5)
                                            data = data + serial.read(serial.inWaiting())
                                            # print(data.decode('utf-8'))
                                            data_judge = data[len(data) - 8:len(data)]
                                            data = str(data).split(",")
                                            # print((bytearray.fromhex(data[4])).decode('utf-8'))
                                            data = (bytearray.fromhex(data[4])).decode('utf-8')
                                            data = json.loads(data)
                                            print("receive:")
                                            print(data)


                    except:
                        pass


            #data = {'order': 'ask', 'latitude': Latitude, "longitude": Longitude}

            '''judge = '0'
            #data = input('Please input the message: ')
            data = {'order':'ask'}
            data = json.dumps(data)
            l=len(data)
            #legal="\r\n0,"+str(len(data))+"\r\n\r\nOK\r\n"'''

            '''if data=="exit":
                while judge != legal.encode('utf-8'):
                    send_data = "AT+NSOST=0,139.199.105.136,25535," + str(len(data)) + "," + (
                    binascii.b2a_hex(str(data).encode('utf-8'))).decode()
                    print(send_data)
                    send_data = send_data + '\r\n'
                    serial.write(send_data.encode())
                    data = serial.read(1)
                    sleep(1)
                    data = data + serial.read(serial.inWaiting())
                    print(data)
                    judge = data[0:13]

                data_judge = '0'
                # sleep(1)
                while data_judge != b'\r\nOK\r\n':
                    send_data = 'AT+NSOCL=0'
                    print(send_data)
                    send_data = send_data + '\r\n'
                    serial.write(send_data.encode())
                    data = serial.read(1)
                    sleep(0.5)
                    data_judge = data + serial.read(serial.inWaiting())
                    print(data_judge)
                #break'''

            '''legal='OK'
            while judge!=legal:
                send_data="AT+NSOST=0,139.199.105.136,25535,"+str(len(data))+","+(binascii.b2a_hex(str(data).encode('utf-8'))).decode()
                print(send_data)
                send_data = send_data + '\r\n'
                serial.write(send_data.encode())
                data=serial.read(1)
                line = ser.read(ser.inWaiting())
                line = line.decode()
                sleep(1)
                line = line.splitlines(True)
                data=data + serial.read(serial.inWaiting())
                data = str(data).split("\\r\\n")
                print(data)
                judge=data[3]

                for x in line:
                    print(x)
                    if x.startswith('$GPGGA'):
                        try:
                            rmc = pynmea2.parse(x)
                            legal = 'OK'
                            position = {'latitude':float(rmc.lat) / 100,"longitude":float(rmc.lon) / 100}
                            position = json.dumps(position)
                            l = len(position)
                            judge='0'
                            while judge != legal:
                                send_data = "AT+NSOST=0,139.199.105.136,25535," + str(len(position)) + "," + (
                                binascii.b2a_hex(str(position).encode('utf-8'))).decode()
                                print(send_data)
                                send_data = send_data + '\r\n'
                                serial.write(send_data.encode())
                                position = serial.read(1)
                                line = ser.read(ser.inWaiting())
                                line = line.decode()
                                sleep(1)
                                line = line.splitlines(True)
                                position = position + serial.read(serial.inWaiting())
                                position = str(position).split("\\r\\n")
                                print(position)
                                judge = position[3]
                            #print("Latitude:  ")
                            #print(float(rmc.lat) / 100)
                            #print("Longitude: ")
                            #print(float(rmc.lon) / 100)
                            # sleep(0.1)

                            break
                        except:
                            pass'''


            data_judge='0'
            #sleep(1)
            while data_judge!=b'\r\nOK\r\n':
                line = ser.read(ser.inWaiting())
                line = line.decode()

                send_data='AT+NSOCL=0'
                print(send_data)
                send_data = send_data + '\r\n'
                serial.write(send_data.encode())
                data=serial.read(1)
                sleep(0.5)
                data_judge=data + serial.read(serial.inWaiting())
                print(data_judge)

        data_judge='0'
        #sleep(1)
        while data_judge!=b'\r\nOK\r\n':
            send_data='AT+NSOCL=0'
            print(send_data)
            send_data = send_data + '\r\n'
            serial.write(send_data.encode())
            data=serial.read(1)
            sleep(0.5)
            data_judge=data + serial.read(serial.inWaiting())
            print(data_judge)

    except:
        data_judge='0'
        #sleep(1)
        print("意外退出")
        while data_judge!=b'\r\nOK\r\n':
            send_data='AT+NSOCL=0'
            print(send_data)
            send_data = send_data + '\r\n'
            serial.write(send_data.encode())
            data=serial.read(1)
            sleep(0.5)
            data_judge=data + serial.read(serial.inWaiting())
            print(data_judge)

    '''while True:
        send_data = input("input a data: ")
        send_data = send_data + '\r\n'
        serial.write(send_data.encode())
        data=serial.read(1)
        sleep(0.5)
        data = (data + serial.read(serial.inWaiting())).decode()
        print(data)'''
