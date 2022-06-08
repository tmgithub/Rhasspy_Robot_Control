#!/usr/bin/env python3
# encoding: utf-8

## Hauptprogramm zur Steuerung der Servos durch Spracheingabe

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
from datetime import datetime, timedelta
import calendar
import augen as AUGE
from gpiozero import LED
from pixel_ring import pixel_ring

from rhasspyhermes.wake import HotwordDetected
import globals

import threading

global apos
#global kt
#global speaker
#speaker = "nobody"
#global aslot[1,2,3]
#global aval[1,2,3]
power = LED(5)
power.on()
pixel_ring.set_brightness(20)
pixel_ring.change_pattern('echo')
#globals.initialize() ### Globale Variablen initialisieren
pixel_ring.listen()

def on_connect(client, userdata, flags, rc): ## Mit dem mosquitto verbinden und intent und hotword subscriben
    print('Connected at ',datetime.now()) 
    mqtt.subscribe('hermes/intent/#')
    mqtt.subscribe('hermes/hotword/#')


def on_message(client, userdata, msg):
    json_data = json.loads(msg.payload.decode('utf-8'))
    #print("json_data: ",json_data)
    print("MSG: ",msg.topic[:14])
    #pixel_ring.off()
    if msg.topic[ :15] == 'hermes/hotword/':
       htword = str(HotwordDetected.get_wakeword_id(msg.topic))

       print("hw: ",htword)
       #print("hw: ",htword[4:6])
       if htword[4:6] == "tm":
           
          globals.speaker = "thomas"
          print("Think: ")
          pixel_ring.think()

          #print("AHAHA")
          #x=threading.Thread(target=thread_listen, args=(1,))
          #x.start()
       elif htword[4:6] == "hm":
         globals.speaker = "heike"
         pixel_ring.listen()
         time.sleep(0.5)
         pixel_ring.off()
       else:
         globals.speaker = htword 
         pixel_ring.listen()
         time.sleep(0.5)
         pixel_ring.off()   
       print("Speaker: ",globals.speaker)
       
    elif msg.topic[ :14] == 'hermes/intent/':
        
       #pixel_ring.off()
       pixel_ring.listen()


       slots = parse_slots(json_data)
       print("Slots: ", slots)
       intentname = json_data['intent']['intentName']
       print("Intentname: ",intentname)
       #print("Anzahl Slots: ",len(slots))        

          
          
mqtt = mqtt.Client() 
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect('localhost', 1883) 
mqtt.loop_forever()