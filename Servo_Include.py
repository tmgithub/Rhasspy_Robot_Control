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


# Import the PCA9685 module.
import Adafruit_PCA9685
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
    global pwm 
    #print("Init")
    try:
        # Alternatively specify a different address and/or bus:
        pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
        #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=3)
        # Set frequency to 60hz, good for servos.
        pwm.set_pwm_freq(60)
#        pwm.set_pwm(channel, 0, 375)
        bereits_initiiert=1
    except Exception as e:
        bereits_initiiert=0
        print(e)
    #print("Init: ", bereits_initiiert)    
#

def move_servo(channel, pulse, slow):
    global bereits_initiiert
    print(pulse,slow)
    #print("Initiert: ", bereits_initiiert)
    if bereits_initiiert == 0:
       initialize_servoboard()
    try:
       servopos=int(read_servopos(channel))
       npulse = servopos - pulse
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
             pwm.set_pwm(channel, 0, i)
             write_servopos(channel,i)
       #      print("after pwm")
             time.sleep(.05)
       else:
       #   print("Else_slow: ") 
          pwm.set_pwm(channel, 0, pulse)
          #print("Hier: ",pulse,slow)
          write_servopos(channel,pulse)

    except Exception as e:
    #   print(e)
       bereits_initiiert=0
       pass  
    
# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
        #print("Channel: ",channel,"Schritte: ",pulse)
        pulse_length = 1000000    #/ 1,000,000 us per second
        pulse_length /= 60       #/ 60 Hz
        #print('{0}us per period'.format(pulse_length))
        pulse_length /= 4096     #/ 12 bits of resolution
        #print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse /= pulse_length
        pwm.set_pwm(channel,0, pulse)


global apos
global kt

def write_servopos(servo,servopos):     # im tmp Verzeichnis die entsprechende Servodatei mit dem Servowert schreiben
    file_servo="/usr/local/tmp/servo"+str(servo)
    #print("Servo : ",file_servo)
    file=open(file_servo,"w")
    file.write(str(servopos))
    file.close()
    logging.info('Servo: %s Pos: %s',servo,servopos)

def read_servopos(servo):       # im tmp Verzeichnis die entsprechende Servodatei lesen
     #print("Bin jetzt hier")
     try:   
        file_servo="/usr/local/tmp/servo"+str(servo)
        #print("Datei : ",file_servo)
        file=open(file_servo,"r")
        #print("Was soll das")
        servopos = int(file.readline())
        file.close()
        logging.info('Servo: %s Pos: %s',servo,servopos)
     except Exception as e:     # wenn die Datei nicht vorhanden ist oder nicht gelesen werden kann den Servowert auf neutral setzen
        print(e)
        logging.info('Servo: %s Pos: %s',servo,servopos)
        servopos = 400
     return servopos

def servo_initial():
# Kopfdrehservo in Mittelstellung bringen    
    move_servo(co.kopf_drehen, co.kopf_drehen_mitte, co.fast)
    write_servopos(co.kopf_drehen, co.kopf_drehen_mitte)

# Kopfhebeservo in Mittelstellung bringen     
    move_servo(co.kopf_heben, co.kopf_heben_mitte, co.fast)
    write_servopos(co.kopf_heben, co.kopf_heben_mitte)
    
# Kopfseitennickservo in Mittelstellung bringen     
    move_servo(co.kopfk, co.kopfk_mitte, co.fast)
    write_servopos(co.kopfk, co.kopfk_mitte)
    
    move_servo(co.linkes_lid, co.li_auge_oeffnen, co.fast)
    write_servopos(co.linkes_lid, co.li_auge_oeffnen)
    
    move_servo(co.rechten_arm, co.neutral, co.fast)
    write_servopos(co.rechten_arm, co.neutral)

    move_servo(co.linken_arm, co.neutral, co.fast)
    write_servopos(co.linken_arm, co.neutral)
 
    move_servo(co.rechtes_lid, co.re_auge_oeffnen, co.fast)
    write_servopos(co.rechtes_lid, co.re_auge_oeffnen)
    
    move_servo(co.linkes_auge_horiz, co.linkes_auge_horiz_mitte, co.fast)
    write_servopos(co.linkes_auge_horiz, co.linkes_auge_horiz_mitte)
    
    move_servo(co.rechtes_auge_horiz, co.rechtes_auge_horiz_mitte, co.fast)
    write_servopos(co.rechtes_auge_horiz, co.rechtes_auge_horiz_mitte)
    
    move_servo(co.linkes_auge_verti, co.linkes_auge_verti_mitte, co.fast)
    write_servopos(co.linkes_auge_verti, co.linkes_auge_verti_mitte)
    
    move_servo(co.rechtes_auge_verti, co.rechtes_auge_verti_mitte, co.fast)
    write_servopos(co.rechtes_auge_verti, co.rechtes_auge_verti_mitte)
    


