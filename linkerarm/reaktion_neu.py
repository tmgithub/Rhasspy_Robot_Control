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
import paho.mqtt.publish as mqttpublish

import time
from datetime import datetime, timedelta
import calendar
import sys
import subprocess

import threading
import globs
# Globale Variablen und Konstanten
import globs
import constant as co

#import single_bewegung_incl as SBEW
import complex_bewegung_incl as CBEW

#Eigene Includes laden
import Servo_Include as SI
#import mylib as MY

global apos

globs.initialize() ### Globale Variablen initialisieren



def on_connect(client, userdata, flags, rc): ## Mit dem mosquitto verbinden und intent und hotword subscriben
    print('reaktion_neu.py Connected at ',datetime.now()) 
    mqtt.subscribe('hermes/linkerArm/#')


def on_message(client, userdata, msg):
        json_data = json.loads(msg.payload.decode('utf-8'))

        #myslots = json_data["slots"]
        #print("Myslots: ",myslots)
        #print("json_data: ",json_data)
        if msg.topic[ :16] == 'hermes/linkerArm':

       #slots = parse_slots(json_data)
         kt=""
         subkt=""
         speed=""
         wenig=""
         ktmp=""
         seite=""
         
         globals()['GL_SLOW']=""
         globals()['GL_KT']=""
         globals()['GL_SUBKT']=""
         globals()['GL_ST']=""
         globals()['GL_VW']=""
         globals()['GL_SUBVW']=""
         globals()['GL_WET']=""
         globals()['GL_ORT']=""
         globals()['GL_SUBWET']=""
         globals()['GL_SUBANZ']=""
         globals()['GL_AKTION']=""
         
         allglobals = globals()
         
         #print(globals())
         for delslotval in allglobals:
          #print("DEl: ",delslotval)
        
             if delslotval[:3] == "GL_":            
            #print("Delslotval: ",delslotval)
                 globals()[delslotval] = ""

         myslots = json_data["slots"]
         #print("Myslots: ",myslots)

         
         for slot in json_data["slots"]:

             tmpslot=slot["slotName"]
             print("----- !!!!!!!!!!!! --------")
             print("tmpslot: ",tmpslot)
             
             tmpvalue=slot["value"]["value"]
             
             print("tmpvalue: ",tmpvalue)
             
             
             if tmpslot[3:8] == "Seite":
                 #print("Seite: ",tmpslot[3:8])
                 seite = tmpvalue
                 #print(" ")
                 #import pdb; pdb.set_trace()
                 #print("seite: ",seite)
             elif tmpslot[3:7] == "SLOW":
                 speed = tmpvalue
                 
             elif tmpslot[3:7] == "ABIT":
                 wenig = tmpvalue
                 
             #print(slot["slotName"]+": "+slot["value"]["value"])
             #print(tmpslot,"--",tmpvalue)

             globals()[tmpslot] = tmpvalue
             print("globals: --",globals()[tmpslot])

             #print(" ")
         #print("Slots: ", slots)
         intentname = json_data['intent']['intentName']
         #print("Intentname: ",intentname)
       
         #import pdb; pdb.set_trace()
         kt = globals()['GL_KT']
         subkt = globals()['GL_SUBKT']
         st = globals()['GL_ST']
         vw = globals()['GL_VW']
         subvw = globals()['GL_SUBVW']
         wet = globals()['GL_WET']
         ort = globals()['GL_ORT']
         subwet = globals()['GL_SUBWET']
         subanz = globals()['GL_SUBANZ']
         subaktion = globals()['GL_AKTION']

         #print("kt: ",kt)


         #    ktmp=placechange({0: str(list(slots.keys())[0]), 1: str(list(slots.keys())[1]), 2: str(list(slots.keys())[2]),3: str(list(slots.keys())[3])},slots)
         try:
             print("Im Try  reaktion_neu.py on_message() ")
             #print("Ktemp: ",ktmp)
             print(" ")
             
             aktion(kt,subkt,seite,speed,wenig,intentname,myslots,subanz,subaktion)
         except Exception as e:
             print(e)


def sprachausgabe(satz):

    print("reaktion_neu.py sprachausgabe(): ",satz)
    tospeak_payload=json.dumps({'text': satz,'siteId': 'default', 'modelId': 'default'})
    print("Sprecher: ",globs.speaker)
    publish("hermes/tts/say",tospeak_payload)
    
def publish(topic,msg):
     #result=mqttpublish.single('hermes/tts/say', payload=json.dumps({'text': msg,'siteId': 'default', 'modelId': 'default'}))
     #print("Msg: mylib.py publish()",msg," Topic: ",topic)

     result=mqttpublish.single(topic,payload=msg,hostname="192.168.5.240",port=1883)

def aktion(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp,intenttmp,myslots,subanz,subaktion):
    print(" ")
    print("IM aktion Modul: reaktion_neu.py|",intenttmp)
# Einzelne Bewegungen    
    if intenttmp == 'senken':
         print("senken: reaktion_neu.py aktion()")
         print(" ")
         #print("wert1: ",wert1,wert1_value,"wert2: ",wert2,wert2_value,"wert3: ",wert3,wert3_value,"wert4: ",wert4,wert4_value)
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)
         SBEW.senke(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp)
         
    elif intenttmp == 'heben':        
         print("heben: reaktion_neu.py aktion()")
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)
         SBEW.hebe(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp)
         
    elif intenttmp == 'drehen':
         print("drehen: reaktion_neu.py aktion()") 
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)     
         SBEW.drehe(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp)
         
    elif intenttmp == 'oeffnen':
         print("oeffnen: reaktion_neu.py aktion()") 
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp) 
         SBEW.oeffne(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp)
        
    elif intenttmp ==  'schliessen':
         print("schliessen: reaktion_neu.py aktion()") 
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp) 
         print(" ")
         SBEW.schliesse(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp) 
        
# komplexe Bewegungen
    elif intenttmp == 'zeigen':
         print("drehen: reaktion_neu.py aktion()") 
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"ANzahl: ",subanz,"Speed: ",speedtmp,"wenig: ",wenigtmp,"aktion: ",subaktion)
         print(" ") 
         CBEW.zeigen(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp,myslots,intenttmp,subanz,subaktion)

            
SI.servo_initial()
sprache="Das Modul linker Arm ist gestartet"    
sprachausgabe('"%s"' %sprache)



mqtt = mqtt.Client() 

mqtt.on_connect = on_connect
print("SOS")
mqtt.on_message = on_message
mqtt.connect('192.168.5.240', 1883) 
mqtt.loop_forever()
