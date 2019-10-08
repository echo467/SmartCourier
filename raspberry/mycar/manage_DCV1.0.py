#!/usr/bin/env python3
"""
Scripts to drive a donkey 2 car

Usage:
    manage.py (drive) [--model=<model>] [--js] [--type=(linear|categorical|rnn|imu|behavior|3d|localizer|latent)] [--camera=(single|stereo)] [--meta=<key:value> ...]
    manage.py (train) [--tub=<tub1,tub2,..tubn>] [--file=<file> ...] (--model=<model>) [--transfer=<model>] [--type=(linear|categorical|rnn|imu|behavior|3d|localizer)] [--continuous] [--aug]


Options:
    -h --help          Show this screen.
    --js               Use physical joystick.
    -f --file=<file>   A text file containing paths to tub files, one per line. Option may be used more than once.
    --meta=<key:value> Key/Value strings describing describing a piece of meta data about this drive. Option may be used more than once.
"""
import os
import time
from time import sleep
from docopt import docopt
import numpy as np
import binascii
import json
import donkeycar as dk

#import parts
from donkeycar.parts.transform import Lambda, TriggeredCallback, DelayedTrigger
from donkeycar.parts.datastore import TubHandler
from donkeycar.parts.controller import LocalWebController, JoystickController
from donkeycar.parts.throttle_filter import ThrottleFilter
from donkeycar.parts.behavior import BehaviorPart
from donkeycar.parts.file_watcher import FileWatcher
from donkeycar.parts.launch import AiLaunch
import RPi.GPIO as GPIO
import serial
import socket
import os
#ssh -fCNL "*:10010:localhost:10086" sice@10.33.32.6  #10086是被连接的本地端口
# skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# skt.connect(('8.8.8.8', 80))
# socketIpPort = skt.getsockname()
# ip = socketIpPort[0]
# print(ip)
# skt.close()
# os.system("ssh -fCNR 10086:"+ip+":8887 sice@10.33.32.6")#10086是连接的外部服务器端口

def drive(cfg, model_path=None, use_joystick=False, model_type=None, camera_type='single', meta=[] ):
    '''
    Construct a working robotic vehicle from many parts.
    Each part runs as a job in the Vehicle loop, calling either
    it's run or run_threaded method depending on the constructor flag `threaded`.
    All parts are updated one after another at the framerate given in
    cfg.DRIVE_LOOP_HZ assuming each part finishes processing in a timely manner.
    Parts may have named outputs and inputs. The framework handles passing named outputs
    to parts requesting the same named input.
    '''
    #zd d
    if model_type is None:
        if cfg.TRAIN_LOCALIZER:
            model_type = "localizer"
        elif cfg.TRAIN_BEHAVIORS:
            model_type = "behavior"
        else:
            model_type = cfg.DEFAULT_MODEL_TYPE
    
    #Initialize car
    V = dk.vehicle.Vehicle()

    #zd d
    #1 ********************************************* camera ********************************************
    inputs = []
    threaded = True
    print("cfg.CAMERA_TYPE", cfg.CAMERA_TYPE)
    if cfg.CAMERA_TYPE == "PICAM":
        from donkeycar.parts.camera import PiCamera
        cam = PiCamera(image_w=cfg.IMAGE_W, image_h=cfg.IMAGE_H, image_d=cfg.IMAGE_DEPTH)
    #zd d
    else:
        raise(Exception("Unkown camera type: %s" % cfg.CAMERA_TYPE))

    V.add(cam, inputs=inputs, outputs=['cam/image_array'], threaded=threaded)


    #2 ********************************************* controller ********************************************
    #This web controller will create a web server that is capable
    #of managing steering, throttle, and modes, and more.
    ctr = LocalWebController()

    if cfg.AUTO_RECORD_ON_THROTTLE and isinstance(ctr, JoystickController):
        #then we are not using the circle button. hijack that to force a record count indication
        def show_record_acount_status():
            rec_tracker_part.last_num_rec_print = 0
            rec_tracker_part.force_alert = 1
        ctr.set_button_down_trigger('circle', show_record_acount_status)

    V.add(ctr, 
          inputs=['cam/image_array'],
          #outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
          outputs=['user/angle', 'user/throttle', 'user/mode', 'recording', 'change_model', 'user/arrival'],
          #outputs=['user/angle', 'user/throttle', 'user/mode', 'recording', 'change_model'], #zd
          threaded=True)

    # ********************************************* communication ********************************************
    class communication_class:
        def __init__(self):
            # ser = serial.Serial("/dev/ttyUSB0", 9600)
            self.serial = serial.Serial('/dev/ttyUSB2', 9600, timeout=3600)
            # serial = serial.Serial('COM9', 9600, timeout=3600)
            if self.serial.isOpen():
                print("open success")
            else:
                print("open failed")

            data_judge = '0'
            while data_judge != b'\r\nOK\r\n':
                send_data = 'AT'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\nOK\r\n':
                send_data = 'AT+CMEE=1'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\nQuectel\r\n\r\nOK\r\n':
                send_data = 'AT+CGMI'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\nBC95HB-02-STD_900\r\n\r\nOK\r\n':
                send_data = 'AT+CGMM'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\nSECURITY,V100R100C10B657SP3\r\n\r\nPROTOCOL,V100R100C10B657SP3\r\n\r\nAPPLICATION,V100R100C10B657SP3\r\n\r\nSEC_UPDATER,V100R100C10B657SP3\r\n\r\nAPP_UPDATER,V100R100C10B657SP3\r\n\r\nRADIO,BC95HB-02-STD_900\r\n\r\nOK\r\n':
                send_data = 'AT+CGMR'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\n+NBAND:8\r\n\r\nOK\r\n':
                send_data = 'AT+NBAND?'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\n+NCONFIG:AUTOCONNECT,TRUE\r\n+NCONFIG:CR_0354_0338_SCRAMBLING,TRUE\r\n+NCONFIG:CR_0859_SI_AVOID,TRUE\r\n+NCONFIG:COMBINE_ATTACH,FALSE\r\n+NCONFIG:CELL_RESELECTION,FALSE\r\n+NCONFIG:ENABLE_BIP,FALSE\r\n\r\nOK\r\n':
                send_data = 'AT+NCONFIG?'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\n+CGSN:869405035846048\r\n\r\nOK\r\n':
                send_data = 'AT+CGSN=1'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\nOK\r\n':
                send_data = 'AT+CFUN=1'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\n460043193006443\r\n\r\nOK\r\n':
                send_data = 'AT+CIMI'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\nOK\r\n':
                send_data = 'AT+CGATT=0'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\n+CGATT:0\r\n\r\nOK\r\n':
                send_data = 'AT+CGATT?'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\nOK\r\n':
                send_data = 'AT+CGATT=1'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\n+CGATT:1\r\n\r\nOK\r\n':
                send_data = 'AT+CGATT?'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = b'\r\n+CSQ:99,99\r\n\r\nOK\r\n'
            while data_judge == b'\r\n+CSQ:99,99\r\n\r\nOK\r\n':
                send_data = 'AT+CSQ'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\n+COPS:0,2,"46000"\r\n\r\nOK\r\n':
                send_data = 'AT+COPS?'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)

            data_judge = '0'
            while data_judge != b'\r\n+CEREG:0,1\r\n\r\nOK\r\n':
                send_data = 'AT+CEREG?'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)
            print('nb-iot initial ok!')
        def update(self):
            while True:
                try:
                    data_judge = '0'
                    # sleep(1)
                    while data_judge != b'\r\n0\r\n\r\nOK\r\n':
                        send_data = 'AT+NSOCR=DGRAM,17,25535,1'
                        print(send_data)
                        send_data = send_data + '\r\n'
                        self.serial.write(send_data.encode())
                        data = self.serial.read(1)
                        sleep(0.5)
                        data_judge = data + self.serial.read(self.serial.inWaiting())
                        print(data_judge)

                    # line = line.splitlines(True)
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
                        self.serial.write(send_data.encode())
                        data = self.serial.read(1)
                        # line = ser.read(ser.inWaiting())
                        # line = line.decode()
                        sleep(2)
                        # line = line.splitlines(True)
                        data = data + self.serial.read(self.serial.inWaiting())
                        data = str(data).split("\\r\\n")
                        print(data)
                        judge = data[3]

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
                            self.serial.write(send_data.encode())
                            data = self.serial.read(1)
                            sleep(1)
                            data = data + self.serial.read(self.serial.inWaiting())
                            # print(data.decode('utf-8'))
                            data_judge = data[len(data) - 8:len(data)]
                            data = str(data).split(",")
                            # print((bytearray.fromhex(data[4])).decode('utf-8'))
                            data = (bytearray.fromhex(data[4])).decode('utf-8')
                            data = json.loads(data)
                            print("receive:")
                            print(data)

                    data_judge = '0'
                    # sleep(1)
                    while data_judge != b'\r\nOK\r\n':
                        # line = ser.read(ser.inWaiting())
                        # line = line.decode()

                        send_data = 'AT+NSOCL=0'
                        print(send_data)
                        send_data = send_data + '\r\n'
                        self.serial.write(send_data.encode())
                        data = self.serial.read(1)
                        sleep(0.5)
                        data_judge = data + self.serial.read(self.serial.inWaiting())
                        print(data_judge)
                except:
                    while data_judge != b'\r\nOK\r\n':
                        send_data = 'AT+NSOCL=0'
                        print(send_data)
                        send_data = send_data + '\r\n'
                        self.serial.write(send_data.encode())
                        data = self.serial.read(1)
                        sleep(0.5)
                        data_judge = data + self.serial.read(self.serial.inWaiting())
                        print(data_judge)


        def run_threaded(self):
            return ['open', 'open', 'open']

        def shuwtdonw(self):
            #关闭socket
            GPIO.cleanup()
            data_judge = '0'
            # sleep(1)
            print("clean udp socket")
            while data_judge != b'\r\nOK\r\n':
                send_data = 'AT+NSOCL=0'
                print(send_data)
                send_data = send_data + '\r\n'
                self.serial.write(send_data.encode())
                data = self.serial.read(1)
                sleep(0.5)
                data_judge = data + self.serial.read(self.serial.inWaiting())
                print(data_judge)


    #communication = communication_class()
    #V.add(communication, inputs=[], outputs=['lock_state', '', ], threaded=True)
    # ********************************************* lock_ctr ********************************************
    class lock_ctr_class:
        def __init__(self):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(36, GPIO.OUT)  # 1
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(38, GPIO.OUT)  # 2
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(40, GPIO.OUT)  # 3
        def run(self, state):
            #1
            if state[0]=='close':
                GPIO.output(36, True)
            else:
                GPIO.output(36, False)

            #2
            if state[1]=='close':
                GPIO.output(38, True)
            else:
                GPIO.output(38, False)

            #3
            if state[2]=='close':
                GPIO.output(40, True)
            else:
                GPIO.output(40, False)
            # for x in range(3): # 0 1 2
            #     if state[x]=='open':
            #         GPIO.output(11+x, False)
            #     else: # close
            #         GPIO.output(11+x, True)
        def shutdown(self):
            GPIO.cleanup()

    #lock_ctr = lock_ctr_class()
    #V.add(lock_ctr, inputs=['lock_state'], outputs=[])
    # ********************************************* throttle filter ********************************************
    #this throttle filter will allow one tap back for esc reverse
    #th_filter = ThrottleFilter()
    #V.add(th_filter, inputs=['user/throttle'], outputs=['user/throttle'])


    #
    #3 ********************************************* PilotCondition ********************************************
    #See if we should even run the pilot module. 
    #This is only needed because the part run_condition only accepts boolean
    class PilotCondition:
        def run(self, mode):
            if mode == 'user':
                return False
            else:
                return True       

    V.add(PilotCondition(), inputs=['user/mode'], outputs=['run_pilot'])
    #zd d


    #4 ********************************************* RecordTracker ********************************************
    def get_record_alert_color(num_records):
        col = (0, 0, 0)
        for count, color in cfg.RECORD_ALERT_COLOR_ARR:
            if num_records >= count:
                col = color
        return col    

    class RecordTracker:
        def __init__(self):
            self.last_num_rec_print = 0
            self.dur_alert = 0
            self.force_alert = 0

        def run(self, num_records):
            if num_records is None:
                return 0
            
            if self.last_num_rec_print != num_records or self.force_alert:
                self.last_num_rec_print = num_records

                if num_records % 10 == 0:
                    print("recorded", num_records, "records")
                        
                if num_records % cfg.REC_COUNT_ALERT == 0 or self.force_alert:
                    self.dur_alert = num_records // cfg.REC_COUNT_ALERT * cfg.REC_COUNT_ALERT_CYC
                    self.force_alert = 0
                    
            if self.dur_alert > 0:
                self.dur_alert -= 1

            if self.dur_alert != 0:
                return get_record_alert_color(num_records)

            return 0

    rec_tracker_part = RecordTracker()
    V.add(rec_tracker_part, inputs=["tub/num_records"], outputs=['records/alert'])

    #zd d

    #IMU  MPU6050
    '''
    if cfg.HAVE_IMU:
    from donkeycar.parts.imu import Mpu6050
    imu = Mpu6050()
    V.add(imu, outputs=['imu/acl_x', 'imu/acl_y', 'imu/acl_z',
        'imu/gyr_x', 'imu/gyr_y', 'imu/gyr_z'], threaded=True)
    '''

    #5 ********************************************* model ********************************************
# important
    def load_model(kl, model_path):
        start = time.time()
        try:
            print('loading model', model_path)
            kl.load(model_path)
            print('finished loading in %s sec.' % (str(time.time() - start)) )
        except Exception as e:
            print(e)
            print('ERR>> problems loading model', model_path)

    def load_weights(kl, weights_path):
        start = time.time()
        try:
            print('loading model weights', weights_path)
            kl.model.load_weights(weights_path)
            print('finished loading in %s sec.' % (str(time.time() - start)) )
        except Exception as e:
            print(e)
            print('ERR>> problems loading weights', weights_path)

    def load_model_json(kl, json_fnm):
        start = time.time()
        print('loading model json', json_fnm)
        from tensorflow.python import keras
        try:
            with open(json_fnm, 'r') as handle:
                contents = handle.read()
                kl.model = keras.models.model_from_json(contents)
            print('finished loading json in %s sec.' % (str(time.time() - start)) )
        except Exception as e:
            print(e)
            print("ERR>> problems loading model json", json_fnm)

    if model_path:
        #When we have a model, first create an appropriate Keras part
        # most time
        kl = dk.utils.get_model_by_type(model_type, cfg)
        # model_type 默认是linear
        model_reload_cb = None

        if '.h5' in model_path:
            #when we have a .h5 extension
            #load everything from the model file
            # most time
            load_model(kl, model_path)

            def reload_model(filename):
                print("reloading start")
                #zd
                V.sudden_control(0)
                #print('***************', V.mem.items())
                #V.mem.put(['angle', 'throttle', 'pilot/angle', 'pilot/throttle', 'user/angle', 'user/throttle'], [0, 0, 0, 0, 0 ,0])
                #print('***************', V.mem.items())
                load_model(kl, filename)
                print('***************\r\nreloading is done\r\n**************\r\n')
            model_reload_cb = reload_model
        else:
            print("ERR>> Unknown extension type on model file!!")
            return

        #these parts will reload the model file, but only when ai is running so we don't interrupt user driving
        #V.add(DelayedTrigger(100), inputs=['modelfile/dirty'], outputs=['modelfile/reload'], run_condition="ai_running")
        #V.add(TriggeredCallback(model_path, model_reload_cb), inputs=["modelfile/reload"], run_condition="ai_running")
        #zd
        #V.add(TriggeredCallback("./models/mypilot_2.h5", model_reload_cb), inputs=["modelfile/reload","change_model"], run_condition="ai_running")
        #V.add(TriggeredCallback("./models/mypilot_2.h5", model_reload_cb), inputs=["modelfile/reload", "change_model"])

        inputs = ['cam/image_array']
        outputs=['pilot/angle', 'pilot/throttle',  'pilot/arrival']

        V.add(kl, inputs=inputs, outputs=outputs, run_condition='run_pilot')

    # ********************************************** turn_delay_trigger ************************************************
    class turn_delay_class:
        def __init__(self, pause_time):
            self.pause = False
            self.trigger = 0
            self.pause_time = pause_time
            self.now_direc = 0
            #self.direc_list = ['S'] #p is pause
            self.direc_list = ['L']
            #self.on = False
        def update(self):
            while 1:
                if self.pause==True:
                    sleep(2)
                    self.pause = False
                if self.trigger==1:
                    #self.on = False
                    #time.sleep(3)
                    #self.on = True
                    time.sleep(self.pause_time)
                    self.trigger = 0
                    self.now_direc +=1

        def run_threaded(self, arrival_signal, mode, has_arrived):
            # >0 = arrive   <0 = not arrive
            if self.pause==True:
                return True, 'P', ''

            if self.trigger==1:
                return True, self.direc_list[self.now_direc], ''

            if mode == 'user':
                self.now_direc = 0
                self.trigger = 0
                self.pause = False
                print('~~~~~~~~~~~~~~~~~~~direction restart')
                return False, '', ''

            if has_arrived=='arrive':
                return False, '', 'arrive'

            if arrival_signal>0:
                # judge arrive
                # print("now is {}".format(self.now_direc))
                # if self.now_direc >= len(self.direc_list):
                #     print("arrive--------------------------")
                #     return False, '', 'arrive'
                if self.now_direc >= len(self.direc_list):
                    print("arrive--------------------------")
                    return False, '', 'arrive'

                self.trigger = 1
                self.pause = True
                print("**************************start turn!!!, now is {}".format(self.direc_list[self.now_direc]))
                return True, self.direc_list[self.now_direc], ''
            else:
                return False, '', ''

        def shutdown(self):
            return

    #turn_delay = turn_delay_class(1.65)
    turn_delay = turn_delay_class(2)
    #V.add(turn_delay, inputs=['pilot/arrival', 'user/mode'], outputs=['turn/mode', 'turn_direction'], run_condition='run_pilot', threaded=True)
    V.add(turn_delay, inputs=['pilot/arrival', 'user/mode', 'arrive_signal'], outputs=['turn/mode', 'turn_direction', 'arrive_signal'], threaded=True)
    # ********************************************** turn_module ************************************************
    class turn_module_class:
        def __init__(self):
            pass
        def run(self, direc):
            if direc=='P': #pause
                return 0, 0
            elif direc=='L':#left
                return -1, 1
            elif direc=='R': #right
                return 1, -1
            elif direc=='S': #straight
                return 0.4, 0.4
            else: #pause
                return 0, 0

        def shutdown(self):
            return

    turn_module = turn_module_class()
    V.add(turn_module, inputs=['turn_direction'], outputs=['turn/angle', 'turn/throttle'], run_condition='run_pilot')
    # pause module input=[] out=[pause/mode]

    #6 ********************************************* DriveMode ********************************************
    #Choose what inputs should change the car.
    class DriveMode:
        def run(self, mode, turn_mode,
                    user_angle, user_throttle,
                    pilot_angle, pilot_throttle,
                    turn_angle, turn_throttle,
                    arrive_signal):
            if turn_mode==True:
                return turn_angle, turn_throttle

            if mode == 'user': 
                return user_angle, user_throttle
            
            elif mode == 'local_angle':
                return pilot_angle, user_throttle
            
            else: # run_pilot
                if arrive_signal=='arrive':
                    return 0, 0
                return 0.3, 0.4
                #return pilot_angle, pilot_throttle * cfg.AI_THROTTLE_MULT
        
    V.add(DriveMode(), 
          inputs=['user/mode', 'turn/mode',
                  'user/angle', 'user/throttle',
                  'pilot/angle', 'pilot/throttle',
                  'turn/angle', 'turn/throttle',
                  'arrive_signal'],
          outputs=['angle', 'throttle'])

    #zd d
    #to give the car a boost when starting ai mode in a race.


    #7 ********************************************* AiRunCondition ********************************************
    class AiRunCondition:
        '''
        A bool part to let us know when ai is running.
        '''
        def run(self, mode):
            if mode == "user":
                return False
            return True

    V.add(AiRunCondition(), inputs=['user/mode'], outputs=['ai_running'])

    #Ai Recording zd d


    #8 ********************************************* Motor ********************************************
    #Drive train setup
# move power
    if cfg.DRIVE_TRAIN_TYPE == "DC_TWO_WHEEL":
        print('DC start!')
        from donkeycar.parts.actuator import TwoWheelSteeringThrottle, Mini_HBridge_DC_Motor_PWM

        LEFT_PID_DIR1 = 11
        LEFT_PID_DIR2 = 13
        LEFT_PWM = 15
        RIGHT_PID_DIR1 = 12
        RIGHT_PID_DIR2 = 16
        RIGHT_PWM = 18

        # left_motor = Mini_HBridge_DC_Motor_PWM(cfg.HBRIDGE_PIN_LEFT_FWD, cfg.HBRIDGE_PIN_LEFT_BWD)
        # right_motor = Mini_HBridge_DC_Motor_PWM(cfg.HBRIDGE_PIN_RIGHT_FWD, cfg.HBRIDGE_PIN_RIGHT_BWD)
        left_motor = Mini_HBridge_DC_Motor_PWM(LEFT_PID_DIR1, LEFT_PID_DIR2, LEFT_PWM)
        right_motor = Mini_HBridge_DC_Motor_PWM(RIGHT_PID_DIR1, RIGHT_PID_DIR2, RIGHT_PWM)
        two_wheel_control = TwoWheelSteeringThrottle()

        V.add(two_wheel_control, 
                inputs=['throttle', 'angle'],
                outputs=['left_motor_speed', 'right_motor_speed'])

        V.add(left_motor, inputs=['left_motor_speed'])
        V.add(right_motor, inputs=['right_motor_speed'])


    #9 ********************************************* tub ********************************************
    #add tub to save data
    '''
     inputs=['cam/image_array',
                'user/angle', 'user/throttle', 
                'user/mode']
    
        types=['image_array',
               'float', 'float',
               'str']
    '''


    inputs = ['cam/image_array',
              'user/angle', 'user/throttle', 'user/arrival',
              'user/mode']

    types = ['image_array',
             'float', 'float', 'float',
             'str']
    th = TubHandler(path=cfg.DATA_PATH)
    tub = th.new_tub_writer(inputs=inputs, types=types, user_meta=meta)
    V.add(tub, inputs=inputs, outputs=["tub/num_records"], run_condition='recording')

    # zd d

    if type(ctr) is LocalWebController:
        print("You can now go to <your pi ip address>:8887 to drive your car.")

    #run the vehicle for 20 seconds

    V.start(rate_hz=cfg.DRIVE_LOOP_HZ, 
            max_loop_count=cfg.MAX_LOOPS)


if __name__ == '__main__':
    args = docopt(__doc__)
    cfg = dk.load_config()
    
    if args['drive']:
        model_type = args['--type']
        camera_type = args['--camera']
        drive(cfg, model_path=args['--model'], use_joystick=args['--js'], model_type=model_type, camera_type=camera_type,
            meta=args['--meta'])
    
    if args['train']:
        from train import multi_train, preprocessFileList
        
        tub = args['--tub']
        model = args['--model']
        transfer = args['--transfer']
        model_type = args['--type']
        continuous = args['--continuous']
        aug = args['--aug']     

        dirs = preprocessFileList( args['--file'] )
        if tub is not None:
            tub_paths = [os.path.expanduser(n) for n in tub.split(',')]
            dirs.extend( tub_paths )

        multi_train(cfg, dirs, model, transfer, model_type, continuous, aug)

