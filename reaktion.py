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
from datetime import datetime, timedelta
import calendar
import sys
import subprocess

import threading

# Globale Variablen und Konstanten
import globs
import constant as co

#LED Ansteuerung
from gpiozero import LED
from pixel_ring import pixel_ring

from rhasspyhermes.wake import HotwordDetected

#Eigene Includes laden
import Servo_Include as SI
import mylib as MY
import smalltalk_incl as SM
import uhrzeit_incl as UHR
import single_bewegung_incl as SBEW
import complex_bewegung_incl as CBEW
import augen as AUGE

 

global apos
subprocess.Popen(['/usr/bin/python3','/usr/local/intent/hermes_sprachausgabe.py'])
time.sleep(4)
globs.initialize() ### Globale Variablen initialisieren
MY.sound_initialize()

#LED Funktion einschalten
power = LED(5)
power.on()

# Pixel Ring initialisieren
pixel_ring.change_pattern('echo')
pixel_ring.set_brightness(5)
pixel_ring.set_color(True,255,255,255)

pixel_ring.listen()

def on_connect(client, userdata, flags, rc): ## Mit dem mosquitto verbinden und intent und hotword subscriben
    print('reaktion.py Connected at ',datetime.now()) 
    mqtt.subscribe('hermes/intent/#')
    mqtt.subscribe('hermes/hotword/#')


def on_message(client, userdata, msg):
    json_data = json.loads(msg.payload.decode('utf-8'))
    #print("KT: ",GL_KT)  
    #print("SLOW: ",GL_SLOW)
    #print("LINKS: ",GL_Seite_LINKS)
    #print("ABIT: ",GL_ABIT) 
    #print("MSG topic: ",msg.topic)
    #print(" ")
    
    if msg.topic[ :15] == 'hermes/hotword/':
       htword = str(HotwordDetected.get_wakeword_id(msg.topic))
       #print("hw: ",htword)
       #print("hw: ",htword[4:6])
       if htword[4:6] == "tm":
          globs.speaker = "thomas"
          pixel_ring.wakeup()
          #print("AHAHA")
          #x=threading.Thread(target=thread_listen, args=(1,))
          #x.start()
       elif htword[4:6] == "hm":
         globs.speaker = "heike"
         pixel_ring.think()
       else:
         globs.speaker = htword 
         pixel_ring.think()
         print("Speaker: ",globs.speaker)
    elif msg.topic[ :14] == 'hermes/intent/':
         #print("Mal sehen: ",json_data)
         #print(" ")
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
         
         allglobals = globals()
         #print(globals())
         
         for delslotval in allglobals:
          #print("DEl: ",delslotval)
        
             if delslotval[:3] == "GL_":            
            #print("Delslotval: ",delslotval)
                 globals()[delslotval] = ""

         myslots = json_data["slots"]
         print("Was geht ab ? ")
         print("Myslots: ",myslots)

         
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
             #print("globals: --",globals()[tmpslot])

             #print(" ")
         #print("Slots: ", slots)
         intentname = json_data['intent']['intentName']
         intentnametmp = json_data['intent']
         print("tintent: ",intentnametmp)
         print(" ")
         print("Intentname: ",intentname)
       
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

         #print("kt: ",kt)


         #    ktmp=placechange({0: str(list(slots.keys())[0]), 1: str(list(slots.keys())[1]), 2: str(list(slots.keys())[2]),3: str(list(slots.keys())[3])},slots)
         try:
             print("Im Try  reaktion.py on_message() ")
             #print("Ktemp: ",ktmp)
             print(" ")
           
             aktion(kt,subkt,seite,speed,wenig,intentname,st,vw,subvw,wet,ort,subwet,myslots,intentnametmp,subanz)
         except Exception as e:
             print(e)
    else:
         pixel_ring.listen()


def aktion(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp,intenttmp,sttmp,vwtmp,subvwtmp,wettmp,orttmp,subwettmp,myslots,intentnametmp,subanztmp):
    print(" ")
    print("IM aktion Modul: reaktion.py|",intenttmp)
# Einzelne Bewegungen    
    if intenttmp == 'senken':
         print("senken: reaktion.py aktion()")
         print(" ")
         #print("wert1: ",wert1,wert1_value,"wert2: ",wert2,wert2_value,"wert3: ",wert3,wert3_value,"wert4: ",wert4,wert4_value)
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)
         SBEW.senke(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp)
         
    elif intenttmp == 'heben':
         print("heben: reaktion.py aktion()")
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)
         SBEW.hebe(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp)
         
    elif intenttmp == 'drehen':
         print("drehen: reaktion.py aktion()") 
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)     
         SBEW.drehe(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp)
         
    elif intenttmp == 'oeffnen':
         print("oeffnen: reaktion.py aktion()") 
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp) 
         SBEW.oeffne(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp)
        
    elif intenttmp ==  'schliessen':
         print("schliessen: reaktion.py aktion()") 
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp) 
         print(" ")
         SBEW.schliesse(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp) 
        
# komplexe Bewegungen
    elif intenttmp == 'zeigen':
         print("zeigen: reaktion.py aktion()") 
         print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)
         print(" ") 
         CBEW.zeigen(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp,myslots,intentnametmp,subanztmp)
               
    elif intenttmp == 'bewegung':
        print("Aktion bewegung: ")

# Verschiedenes
    elif intenttmp == 'LICHT':
         print("Hier geht das Licht los: in reaktion.py")       
         MY.licht(wert1,wert1_value)
         
    elif intenttmp == 'rechnen':
         print("Hier geht das Rechnen los: in reaktion.py")        
         MY.rechnen(wert1_value,wert2,wert2_value,wert3_value)
                           
    elif intenttmp == 'SmallTalk':     
        print("Hier geht der Smalltalk los: in reaktion.py")
        SM.sprueche(sttmp,vwtmp,subvwtmp)
                
    elif intenttmp == 'Uhrzeit':
        print("Hier geht dier Uhrzeit los: in reaktion.py")
        UHR.uhrzeit(wert1,wert1_value,wert2,wert2_value)
        
    elif intenttmp == 'wetter':
        
        print("Hier geht das Wetter los: in reaktion.py")
        MY.wetter(wettmp,orttmp,subwettmp)
        
    elif intenttmp == 'wecker':
        print("Hier geht der Wecker los: in reaktion.py")

    elif intenttmp == 'Wohlbefinden':
        
        print("Hier ist das Wohlbefinden: in reaktion.py")
        
        sprache = "Das habe ich nicht verstanden" ## Falls die Funktion einen Wert hat den die IF-clause nicht kennt
                
        temp= MY.wohlbefinden() 
        
        Maxram = MY.getRAMinfo()[0]+ " GigaByte "
        Freeram = MY.getRAMinfo()[1]+ " GigaByte "

        
        if sttmp == "CPUHEAT":
           sprache = "Mir geht es gut . Die Temperatur des Prozessors beträgt "+str(temp)+" Grad. Und das ist innerhalb der normalen Parameter"
           
        elif sttmp == "SPEICHER":
            sprache = "Der Speicher beträgt "+Maxram+ ". Und davon sind "+Freeram+" frei" 
              
        elif sttmp == "KOMPLETHEALTH":
            sprache = "Mir geht es gut. Die Temperatur des Prozessors beträgt "+str(temp)+" Grad . Und das ist innerhalb der normalen Parameter Der Speicher beträgt "+Maxram+ " und davon sind "+Freeram+" frei"
            
        elif sttmp ==   "WASGEHT":
            sprache = "Es geht so. Die CPU-Temperatur ist "  +str(temp)+ " Grad und das ist okay"
            


            
        MY.sprachausgabe('"%s"' %sprache)
        
        
        
        
        #wecker()


            

def parse_slots(wert):
    '''
    We extract the slots as a dict
    '''
    #data = json.loads(msg) # .payload
    data = wert 
    return dict((slot['slotName'], slot['value']) for slot in data['slots'])

def placechange(nameslot,slots):
    global kt
    global seite
    global speed
    global wenig
    global real_speed
    global real_seite
    global real_wenig
    kt=""
    seite=""
    speed=""
    wenig=""
    real_speed=""
    real_seite=""
    real_wenig=""
    print("Place change in reaktion.py plachechange()")
    try:
        for i in range(len(nameslot)):
            #print("Nameslot: ",nameslot[i])
            if "KT" in nameslot[i]:
                kt = (slots[nameslot[i]])['value']
            elif "ReLi" in nameslot[i] or "RECHTS" in nameslot[i] or "LINKS" in nameslot[i]:    
                seite = (slots[nameslot[i]])['value']
                #real_seite = (slots[nameslot[i]])['value']
                #print("Reale Seite: ",seite)
            elif "SLOW" in nameslot[i]:
                speed = (slots[nameslot[i]])['value']
                #real_speed="langsam"
            elif "WENIG" in nameslot[i]:
                wenig = (slots[nameslot[i]])['value']
                #real_wenig="ein wenig"
        #print("fori: ",kt,seite)
        
    except Exception as e:
        print(e)
    print("KT: ",kt,"Seite: ",real_seite,"Speed: ",real_speed,wenig,real_speed,real_wenig)
    return kt,seite,speed,wenig
     




            
SI.servo_initial()

nline="Spracherkennung eingeschaltet"
MY.sprachausgabe('"%s"' %nline)
temp= MY.wohlbefinden()
#print("SW",temp)
sprache = "Die Temperatur des Prozessors beträgt "+str(temp)+" Grad"
#MY.sprachausgabe('"%s"' %sprache)

Maxram = MY.getRAMinfo()[0]+ " GigaByte "
Freeram = MY.getRAMinfo()[1]+ " GigaByte "
sprache = "Der Speicher beträgt "+Maxram+ " und davon sind "+Freeram+" frei"
#MY.sprachausgabe('"%s"' %sprache)


mqtt = mqtt.Client() 
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect('localhost', 1883) 
mqtt.loop_forever()
