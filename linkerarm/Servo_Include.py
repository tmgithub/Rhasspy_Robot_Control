#!/usr/bin/env python3
# encoding: utf-8
from __future__ import print_function
from __future__ import division
import paho.mqtt.client as mqtt 
import json
import logging
from random import randint
import os
import glob
import time
import constant as co
import sys

from adafruit_servokit import ServoKit
global bereits_initiiert
bereits_initiiert = 0
#import platform
logging.basicConfig(filename='/var/log/mypython.log',format='%(asctime)s - %(message)s',filemode='w', level=logging.INFO)
#sys.s
# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685()
def initialize_servoboard():
    global bereits_initiiert
    global kit 
    #print("Init")
    try:
        kit = ServoKit(channels=16)
        bereits_initiiert=1
    except Exception as e:
        bereits_initiiert=0
        print(e)
    #print("Init: ", bereits_initiiert)    
#

def move_servo(servonumber, degree, slow):
    global bereits_initiiert
    print(degree,slow)
    #print("Initiert: ", bereits_initiiert)
    if bereits_initiiert == 0:
       initialize_servoboard()
    try:
       servopos=int(read_servopos(servonumber))
       npulse = servopos - degree
       if npulse < 0:
          step = 5 
       elif npulse > 0: 
          step = -5
       elif npulse == 0:
          step = 1  
       if slow == "True":
       #     print(pulse,  servopos, step)
            for i in range(servopos, pulse+step, step):
           #for i in range(pulse, servopos, step):
#             print(pulse, servopos, step, i)
             kit.servo[servonumber].angle = i 
             write_servopos(servonumber,i)
       #      print("after pwm")
             time.sleep(.05)
       else:
       #   print("Else_slow: ") 
          kit.servo[servonumber].angle = degree
          #pwm.set_pwm(servonumber, 0, pulse)
          #print("Hier: ",pulse,slow)
          write_servopos(servonumber,pulse)

    except Exception as e:
    #   print(e)
       bereits_initiiert=0
       pass  
    
# Helper function to make setting a servo pulse width simpler.



global apos
global kt

def write_servopos(servonumber,servodegree):     # im tmp Verzeichnis die entsprechende Servodatei mit dem Servowert schreiben
    file_servo="/usr/local/tmp/servo"+str(servonumber)
    #print("Servo : ",file_servo)
    file=open(file_servo,"w")
    file.write(str(servodegree))
    file.close()
    logging.info('Servo: %s Pos: %s',servonumber,servodegree)

def read_servopos(servonumber):       # im tmp Verzeichnis die entsprechende Servodatei lesen
     #print("Bin jetzt hier")
     try:   
        file_servo="/usr/local/tmp/servo"+str(servonumber)
        #print("Datei : ",file_servo)
        file=open(file_servo,"r")
        #print("Was soll das")
        servodegree = int(file.readline())
        file.close()
        logging.info('Servo: %s Pos: %s',servonumber,servodegree)
     except Exception as e:     # wenn die Datei nicht vorhanden ist oder nicht gelesen werden kann den Servowert auf neutral setzen
        print(e)
        logging.info('Servo: %s Pos: %s',servonumber,servodegree)
        servodegree = 178
     return servodegree

def servo_initial():
# Kopfdrehservo in Mittelstellung bringen 
   
    move_servo(co.zfinger, co.zfinger_gerade, co.fast)
    write_servopos(co.zfinger, co.zfinger_gerade)
    
    move_servo(co.mfinger, co.mfinger_gerade, co.fast)
    write_servopos(co.mfinger, co.mfinger_gerade)
    
    move_servo(co.rfinger, co.rfinger_gerade, co.fast)
    write_servopos(co.rfinger, co.rfinger_gerade)
    
    move_servo(co.kfinger, co.kfinger_gerade, co.fast)
    write_servopos(co.kfinger,co.kfinger_gerade)
    
   # move_servo(co.daumen, co.servo_max, co.fast)
   # write_servopos(co.daumen, co.servo_max)
    
    
  #  kit.servo[0].angle = 178 #Mfinger gestreckt
  #  time.sleep(1)
  #  #kit.servo[1].angle = 46
  #  kit.servo[2].angle = 178
  #  time.sleep(1)
  #  kit.servo[3].angle = 46

 

    


