#!/usr/bin/env python3
# encoding: utf-8
from __future__ import print_function
from __future__ import division
import paho.mqtt.client as mqtt
import json
from random import randint
import os
import glob
import time
import constant as co
import sys
import Servo_Include as SI
import mylib as MY
import smalltalk_incl as SM
from datetime import datetime, timedelta
import calendar
import Adafruit_PCA9685

def initialize_servoboard(channel,pulse):
    global pwm
    try:
       # Alternatively specify a different address and/or bus:
       pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=3)
       # Set frequency to 60hz, good for
       pwm.set_pwm_freq(50)
       pulse_length = 1000000    #/ 1,000,000 us per second
       pulse_length /= 50       #/ 60 Hz
       pulse_length /= 4096     #/ 12 bits of resolution
       pulse *= 1000
       pulse /= pulse_length
       pulse =int(pulse)
       pwm.set_pwm(channel, 0, pulse)
    except Exception as e:
       print(e)


initialize_servoboard(8,250)
initialize_servoboard(9,250)
initialize_servoboard(10,250)
initialize_servoboard(12,250)
initialize_servoboard(13,250)
initialize_servoboard(8,550)
