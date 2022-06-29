from __future__ import print_function
from __future__ import division
import paho.mqtt.client as mqtt
import json
#from random import randint
#import os
#import glob
import subprocess


from datetime import datetime, timedelta

import sys

import threading


def on_connect(client, userdata, flags, rc): ## Mit dem mosquitto verbinden und intent und hotword subscriben
    print('hermes Sprachausgabe Connected at ',datetime.now()) 
    mqtt.subscribe('hermes/tts/say')
    
def on_message(client, userdata, msg):
    json_data = json.loads(msg.payload.decode('utf-8'))
    #print("json_data: ",json_data)
    #print("MSG: ",msg.topic)
#'hermes/tts/say' -m '{"text": "Ciao!", "lang": "it_IT"}'
    if msg.topic == 'hermes/tts/say':
       satz = json_data['text']
       #print("satz: ",satz)
       sprachausgabe(satz)
       
def sprachausgabe(satz):
    print("hermes_sprachausgabe.py sprachausgabe(): ",satz)

    syssentence = "/usr/bin/espeak-ng -d plughw:0,0 -v mb-de6 -k 20 -p 60 -s 140 -a 180 -w /tmp/soundout.wav " + satz
    sysplay = "/usr/bin/aplay -q -D plughw:0,0 /tmp/soundout.wav"

    subprocess.run(syssentence,shell=True,stdout=subprocess.DEVNULL)
    subprocess.run(sysplay,shell=True,stdout=subprocess.DEVNULL)


       
mqtt = mqtt.Client() 
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect('localhost', 1883) 
mqtt.loop_forever()
