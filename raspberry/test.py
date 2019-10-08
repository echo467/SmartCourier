import os
import serial
from time import sleep
import json
import binascii

def judge_iot(usbx):
    for x in range(5):
        send_data = r'AT\r\n'
        usbx.write(send_data.encode())
        recv = usbx.read(1)
        sleep(0.5)
        data_judge = recv + usbx.read(usbx.inWaiting())
        if data_judge==b'\r\nOK\r\n':
            return True
    return False

usb = os.popen('ls /dev/ttyUSB*')
usb = usb.read()
usb = usb.split()
if len(usb)==1:
    #print("error:USB num is {}".format(len(usb)))
    nb_iot = serial.Serial(usb[0], 9600)

    data_judge = '0'
    while data_judge != b'\r\nOK\r\n':
        send_data = 'AT+CMEE=1'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\nQuectel\r\n\r\nOK\r\n':
        send_data = 'AT+CGMI'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\nBC95HB-02-STD_900\r\n\r\nOK\r\n':
        send_data = 'AT+CGMM'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\nSECURITY,V100R100C10B657SP3\r\n\r\nPROTOCOL,V100R100C10B657SP3\r\n\r\nAPPLICATION,V100R100C10B657SP3\r\n\r\nSEC_UPDATER,V100R100C10B657SP3\r\n\r\nAPP_UPDATER,V100R100C10B657SP3\r\n\r\nRADIO,BC95HB-02-STD_900\r\n\r\nOK\r\n':
        send_data = 'AT+CGMR'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\n+NBAND:8\r\n\r\nOK\r\n':
        send_data = 'AT+NBAND?'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\n+NCONFIG:AUTOCONNECT,TRUE\r\n+NCONFIG:CR_0354_0338_SCRAMBLING,TRUE\r\n+NCONFIG:CR_0859_SI_AVOID,TRUE\r\n+NCONFIG:COMBINE_ATTACH,FALSE\r\n+NCONFIG:CELL_RESELECTION,FALSE\r\n+NCONFIG:ENABLE_BIP,FALSE\r\n\r\nOK\r\n':
        send_data = 'AT+NCONFIG?'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\n+CGSN:869405035846048\r\n\r\nOK\r\n':
        send_data = 'AT+CGSN=1'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\nOK\r\n':
        send_data = 'AT+CFUN=1'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\n460043193006443\r\n\r\nOK\r\n':
        send_data = 'AT+CIMI'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\nOK\r\n':
        send_data = 'AT+CGATT=0'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\n+CGATT:0\r\n\r\nOK\r\n':
        send_data = 'AT+CGATT?'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\nOK\r\n':
        send_data = 'AT+CGATT=1'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\n+CGATT:1\r\n\r\nOK\r\n':
        send_data = 'AT+CGATT?'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = b'\r\n+CSQ:99,99\r\n\r\nOK\r\n'
    while data_judge == b'\r\n+CSQ:99,99\r\n\r\nOK\r\n':
        send_data = 'AT+CSQ'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\n+COPS:0,2,"46000"\r\n\r\nOK\r\n':
        send_data = 'AT+COPS?'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    data_judge = '0'
    while data_judge != b'\r\n+CEREG:0,1\r\n\r\nOK\r\n':
        send_data = 'AT+CEREG?'
        print(send_data)
        send_data = send_data + '\r\n'
        nb_iot.write(send_data.encode())
        data = nb_iot.read(1)
        sleep(0.5)
        data_judge = data + nb_iot.read(nb_iot.inWaiting())
        print(data_judge)

    try:
        while True:
            data_judge = '0'
            sleep(1)
            #create udp socket
            while data_judge != b'\r\n0\r\n\r\nOK\r\n':
                send_data = 'AT+NSOCR=DGRAM,17,25535,1'
                print(send_data)
                send_data = send_data + '\r\n'
                nb_iot.write(send_data.encode())
                data = nb_iot.read(1)
                sleep(0.5)
                data_judge = data + nb_iot.read(nb_iot.inWaiting())
                print(data_judge)

            # send data
            legal = 'OK'
            data = {'order': 'ask'}
            data = json.dumps(data)
            l = len(data)
            judge = '0'
            while judge != legal:
                send_data = "AT+NSOST=0,139.199.105.136,25535," + str(len(data)) + "," + (
                    binascii.b2a_hex(str(data).encode('utf-8'))).decode()
                print(send_data)
                send_data = send_data + '\r\n'
                nb_iot.write(send_data.encode())
                data = nb_iot.read(1)
                #line = ser.read(ser.inWaiting())
                #line = line.decode()
                sleep(2)
                #line = line.splitlines(True)
                data = data + nb_iot.read(nb_iot.inWaiting())
                data = str(data).split("\\r\\n")
                print(data)
                judge = data[3]
            #receive data
            if len(data) > 5:
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
                    nb_iot.write(send_data.encode())
                    data = nb_iot.read(1)
                    sleep(1)
                    data = data + nb_iot.read(nb_iot.inWaiting())
                    # print(data.decode('utf-8'))
                    data_judge = data[len(data) - 8:len(data)]
                    data = str(data).split(",")
                    # print((bytearray.fromhex(data[4])).decode('utf-8'))
                    data = (bytearray.fromhex(data[4])).decode('utf-8')
                    data = json.loads(data)
                    print("receive:")
                    print(data)
            # release udp socket
            data_judge = '0'
            # sleep(1)
            while data_judge != b'\r\nOK\r\n':
                #line = ser.read(ser.inWaiting())
                #line = line.decode()
                send_data = 'AT+NSOCL=0'
                print(send_data)
                send_data = send_data + '\r\n'
                nb_iot.write(send_data.encode())
                data = nb_iot.read(1)
                sleep(0.5)
                data_judge = data + nb_iot.read(nb_iot.inWaiting())
                print(data_judge)
    except:
        data_judge = '0'
        # sleep(1)
        print("意外退出")
        while data_judge != b'\r\nOK\r\n':
            send_data = 'AT+NSOCL=0'
            print(send_data)
            send_data = send_data + '\r\n'
            nb_iot.write(send_data.encode())
            data = nb_iot.read(1)
            sleep(0.5)
            data_judge = data + nb_iot.read(nb_iot.inWaiting())
            print(data_judge)

elif len(usb)==2:
    try:
        # select true socket
        tmp1 = serial.Serial(usb[0], 9600)
        tmp2 = serial.Serial(usb[1], 9600)
        if (tmp1.is_open() and tmp2.is_open()):
            print("open ok")
        else:
            print("open error")
            raise ValueError

        #judge
        if judge_iot(tmp1):
            nb_iot = tmp1
            gps = tmp2
        elif judge_iot(tmp2):
            nb_iot = tmp2
            gps = tmp1
        else:
            print("no no-iot!")
            raise ValueError

        #init nb-iot

        # build udp socket

        #send data and receive data


    except:
        print("erorr!")
else:
    print(len(usb))

