#! /usr/bin/python3

# import the necessary packages
#from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
#from picamera.array import PiRGBArray
#from picamera import PiCamera
#import argparse
#import imutils
import time
import cv2
import RPi.GPIO as GPIO
import sqlite3
import configparser
import os
import re

import base64
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES



path = "/home/pi/Desktop/settings.ini"

def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "startPos", "2.5")
    config.set("Settings", "targetPos", "10")
    config.set("Settings", "servoPin", "22")
    config.set("Settings", "frequencyServo", "50")
    config.set("Settings", "servoTime", "5")

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    return float(value)


def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    value=str(value)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)

def update_setting_full(path, section, data):
    """
    Update a setting
    """
    nums = re.findall(r'\d*\.\d+|\d+', data)

    nums = [float(i) for i in nums]
    config = get_config(path)
    startpos = str(nums[0])
    targetpos = str(nums[1])
    servopin = str(nums[2])
    frequencyservo = str(nums[3])
    servotime = str(nums[4])
    config.set(section, "startpos", startpos)
    config.set(section, "targetpos", targetpos)
    config.set(section, "servopin", servopin)
    config.set(section, "frequencyservo", frequencyservo)
    config.set(section, "servotime", servotime)
    with open(path, "w") as config_file:
        config.write(config_file)

class LED:
    def __init__(self):
        self.pin = 37
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def close(self):
        GPIO.cleanup()

class ServoAct:
    def __init__(self):
        self.startPos = get_setting(path, 'Settings', 'startPos')#2.5 as 0 degree
        self.targetPos = get_setting(path, 'Settings', 'targetPos')
        self.holdTime = 0.0
       
        servo = int(get_setting(path, 'Settings', 'servopin'))

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo, GPIO.OUT)
        
        self.p = GPIO.PWM(servo, 50) #50 freq
        #self.close()
        self.p.start(self.startPos)
        time.sleep(0.3)
        self.hold()
        #self.close()
    
    def start(self):
        servo = int(get_setting(path, 'Settings', 'servopin'))
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo, GPIO.OUT)
        self.p = GPIO.PWM(servo, 50) #50 freq        
        self.p.start(self.startPos)
        time.sleep(0.2)
        self.hold()
    
    def setActPosition(self):
        self.targetPos = get_setting(path, 'Settings', 'targetPos')
        self.p.ChangeDutyCycle(self.targetPos)
        
    def setIdlePosition(self):
        self.startPos = get_setting(path, 'Settings', 'startPos')
        self.p.ChangeDutyCycle(self.startPos)
    
    def setPosition(self, pos):
        #5-10 
        p.ChangeDutyCycle(pos)
        # in servo motor,
        # 1ms pulse for 0 degree (LEFT)
        # 1.5ms pulse for 90 degree (MIDDLE)
        # 2ms pulse for 180 degree (RIGHT)

        # so for 50hz, one frequency is 20ms
        # duty cycle for 0 degree = (1/20)*100 = 5%
        # duty cycle for 90 degree = (1.5/20)*100 = 7.5%
        # duty cycle for 180 degree = (2/20)*100 = 10%
        #hard video code
    
    def hold(self):
        self.p.ChangeDutyCycle(0.0)
        #setTargetPos
        #Timer
        #setStartPos
        
    def close(self):
        self.p.stop()
        GPIO.cleanup()

class QRCheck:#проверка правильности
    
    def __init__(self):
        self.subd = SUBD()
        self.last = None
        self.list1 = ['6', 'T', '3', 'S','R', '9', 'N','E', 'W', 'Z', 'M', 'A',
                     'U', 'V', 'L', '2', 'F', 'P', 'G', 'C', 'B', '0',
                     'H', 'K', 'G', 'D', 'I', 'X', 'O', '8', 'Y','Q']
        
        self.list2 = ['x','s','r', 'm', 'w', '1', 'o', 'q', 'p', 'n', 'a', 'd',
                      'h', 'i', '4', 'e', '7', 'v', 'b', 'l','z','u', 'c', 'f',
                      'g', 'j', 'k', 't', '5','y']
        
    
    def applyLast(self):
        if self.last is not None:
            self.subd.add(self.last)
        else:
            print("Null last")
    
    def check(self, data):
        
        result = 0
        
        ##datab64=base64.b64decode(data)
        #private_key = RSA.importKey(open('privkeycrypto.pem').read())
        #sentinel = Random.new().read(24)
        #cipher_rsa = PKCS1_v1_5.new(private_key)
        #message = cipher_rsa.decrypt(datab64,sentinel)
        try:
            key = b'YOURKEYGYOURKEYG'
            ciphered_data = base64.b64decode(data)
            cipher = AES.new(key, AES.MODE_ECB) # CFB mode
            result = unpad(cipher.decrypt(ciphered_data), 16)
            data=str(result,'utf-8')

            d = list(data)
        except Exception:
            result = -1  # incorrect
            return result
        
        if(str(data)=="0"):
            result = -3 #admin
            return result

        if (str(data)[:4] == "1518"):
            time = int(str(data)[4:])
            result = -time #settings
            return result

        if (str(data) == "666"):
            result = -4  #destroy
            return result

        if (str(data)[:4] == "1537"):
            update_setting_full(path, "Settings", str(data)[4:])
            result = -5 #settings
            return result
        """
        numd = []
        val = None
        
        for i in range(0, len(d)):
            
            try:
              val = self.list1.index(d[i])
            except Exception:
                print('no first')
                try:
                    val = self.list2.index(d[i])
                    val = -val
                except Exception:
                    print('no second')
                    val = None
                    result = -1
                    return result
            numd.append(val)
        print(numd)  
        
        if len(d)==16:
            result = 1
        else:
            result = -1 #incorrect
            return result
        
        c1 = int(numd[1]) + int(numd[7])+int(numd[3])
        c2 = int(numd[1]) + int(numd[15])-int(numd[12])
        
        print(c1)
        print(c2)
        
        if c1==15:
            result = 1
        else:
            result = -1 #incorrect
            return result  
          
        if c2==4:
            result = 1
        else:
            result = -1 #incorrect
            return result   
        """
         
        #algorithm_check_1
        
        if len(d)==10:
            result = 1
        else:
            result = -1 #incorrect
            return result
        
        if d[0]=='1':
            result = 1
        else:
            result = -1 #incorrect
            return result
        
        #algorithm_check_2
        if not self.subd.lookFor(data):
            result = 1
        else:
            result = -2 #used
            return result
        #usage check
        self.last = data
        return result

    def close(self):
        self.subd.close()
        self.last = None

class SUBD:    
    def __init__(self):
        self.conn=None
        self.curs=None
        
    def lookFor(self, data):
        sql = "SELECT * FROM qrs WHERE qr=?"

        if self.conn is None:
            self.conn=sqlite3.connect('qrdata.db')
            self.curs=self.conn.cursor()
        
        self.curs.execute(sql, [(data)])
        count = len(self.curs.fetchall())
        print(data + ' found: ' + str(count))
        if count == 0:
            return False
        else:
            return True
        
    def add(self, data):
        sql = "INSERT INTO qrs VALUES ('" + data + "')"
        self.curs.execute(sql)
        self.conn.commit()
        print(data + ' added')

    def close(self):
        if self.conn is not None:   
            self.conn.close()
            self.conn=None
            self.curs=None
        
        
class QRDetect:#класс распознования кода
    def __init__(self):
        self.detector = cv2.QRCodeDetector()
        
    def detect(self, img): 
        
        data, bbox, _ = self.detector.detectAndDecode(img)
    
        if bbox is not None:    
            """
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
                
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            """
            if data:
                return data
        return None
    
    
class CameraCapture: # класс картинки с камеры
    def __init__(self):
        self.vs = None
        self.fps = None
        self.capture = False
        
    def start(self):
        self.vs = PiVideoStream().start()
        time.sleep(0.1)
        self.capture = True
        fps = FPS().start()
        print("Camera started")
        
    def stop(self):
        self.capture = False
        self.vs.stop()    
        print("Camera stopped")
    
    def getFrame(self):
        if self.capture:
            return self.vs.read()
        else:
            return None





"""
checkMode = True

cc = CameraCapture()
qrd = QRDetect()
qrc = QRCheck()


cc.start()

while checkMode:
    frame = cc.getFrame()
    qrData = qrd.detect(frame)
    
    if qrData:
        print(qrData)
        qrResult = qrc.check(qrData)  
        if qrResult == -1:
            print("Invalid code")
            #4 sec wait
            checkMode = False
        elif qrResult == -2:
            print("Code already used")
            #4 sec wait
            checkMode = False
        elif qrResult == 1:
            print("Code is valid")
            #Servo go
            checkMode = False
        
    #frame = cv2.resize(frame, (1280, 720))    
        
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
"""

"""
s = ServoAct()
time.sleep(5)
#s.start()
s.setActPosition()
time.sleep(3)
s.setIdlePosition()
time.sleep(3)
s.close()
"""

