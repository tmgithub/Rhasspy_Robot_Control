  #!/usr/bin/env python3
# encoding: utf-8
from __future__ import absolute_import, division, unicode_literals, print_function
from __future__ import division
import paho.mqtt.client as mqtt 
import json
from random import randint
import os
import glob
import time
import sys
import calendar
import datetime
from datetime import timedelta
import importlib
import requests


import constant as co
import Servo_Include as SI
import mylib as MY

import sys
if sys.version_info.major < 3:
    import thread as _thread
else:
    import _thread
from time import sleep
#importlib.reload(sys)

"""
Created on Tue Jul 18 15:42:02 2017

@author: josef
"""


def inkey():
    import tty, termios
    global char
    fd=sys.stdin.fileno()
    remember_attributes=termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    char=sys.stdin.read(1) # wir lesen nur einzelne zeichen
    termios.tcsetattr(fd,termios.TCSADRAIN, remember_attributes)
    
def main():
    SI.servo_initial()
    global char
    char = None
    _thread.start_new_thread(inkey, ())
    speed = 350 #Setting the speed to 50 default
    while True:
        if char is not None:
            if speed > 200 and speed < 550:
                try:
                    print("Key pressed is " + char.decode('utf-8'))

                except UnicodeDecodeError:
                    print("character can not be decoded, sorry!")
                    char = None
                _thread.start_new_thread(inkey, ())
                if char == 'q' or char == '\x1b':  # x1b is ESC
                    exit()
                elif char == 'a':
                    speed = speed + 10 #Change speed by 1
                    time.sleep(1)
                elif char == 'd':
                    speed = speed - 10
                    time.sleep(1)
                print("Speed : ",speed)                        
#                SI.move_servo(co.kopfk, speed, co.fast) # 320
#                SI.move_servo(co.rechtes_auge_horiz, speed, co.fast)
#                SI.move_servo(co.linkes_lid, speed, co.fast)
                SI.move_servo(co.rechtes_auge_, speed, co.fast)
#                SI.move_servo(co.rechtes_auge_horiz, speed, co.fast)
                char = None
        #print("Program is running")
        sleep(1)

if __name__ == "__main__":
    main()

            
            
#SI.move_servo(co.kopfd, 310, co.slow)
#SI.write_servopos(co.kopfd, 310)

#SI.move_servo(co.kopfk, 340, co.slow)
#SI.write_servopos(co.kopfk, 340)

#SI.move_servo(co.linkes_auge_verti, 350, co.fast)
#SI.write_servopos(co.linkes_auge_verti, 350)
#SI.move_servo(co.linkes_auge_verti,350, co.slow)

#SI.move_servo(co.rechtes_auge_verti, 300, co.fast)
#SI.write_servopos(co.rechtes_auge_verti, 300)
#SI.move_servo(co.rechtes_auge_verti,400, co.slow)

#SI.move_servo(co.rechtes_auge_horiz, 350, co.fast)
#SI.write_servopos(co.rechtes_auge_horiz, 350)
#time.sleep(1)
#SI.move_servo(co.rechtes_auge_horiz,500, co.slow)
#time.sleep(1)
#SI.move_servo(co.rechtes_auge_horiz,250, co.slow)


#SI.move_servo(co.linkes_auge_horiz, 300, co.fast)
#SI.write_servopos(co.linkes_auge_horiz, 300)
#SI.move_servo(co.linkes_auge_horiz,400, co.slow)

