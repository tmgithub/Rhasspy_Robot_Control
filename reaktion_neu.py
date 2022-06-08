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

#Eigene Includes laden
import Servo_Include as SI
import mylib as MY

global apos

globs.initialize() ### Globale Variablen initialisieren



def on_connect(client, userdata, flags, rc): ## Mit dem mosquitto verbinden und intent und hotword subscriben
    print('reaktion.py Connected at ',datetime.now()) 
    mqtt.subscribe('hermes/linkerArm/#')


def on_message(client, userdata, msg):
       json_data = json.loads(msg.payload.decode('utf-8'))

       myslots = json_data["slots"]
    #print("Myslots: ",myslots)
       print("Slots: ")

       for slot in json_data["slots"]:
            tmpslot=slot["slotName"]
            tmpvalue=slot["value"]["value"]
            #print(type(tmpslot))
            print(slot["slotName"]+": "+slot["value"]["value"])
            print(tmpslot,"--",tmpvalue)

            globals()[tmpslot] = tmpvalue

            print(" ")

       #slots = parse_slots(json_data)
       #print("Slots: ", slots)
       intentname = json_data['intent']['intentName']
       print("Intentname: ",intentname)
       #print("Anzahl Slots: ",len(slots))        

          
       kt=""
       seite = ""
       speed=""
       wenig=""
       wert1 =""
       wert1_value=""
       wert2 =""
       wert2_value=""
       wert3 =""
       wert3_value=""
       wert4 =""
       wert4_value=""
       ktmp=""
    #if len(slots) == 0:
    #    print("0 Slots im On Message: ")
    #    #kt=""
    #    #wert1=""
    #    #wert1_value=""
       #if len(slots) == 1:
       #    print("1 Slots im On Message: ")
       #    wert1 = str(list(slots.keys())[0])
       #    wert1_value = slots[wert1]['value']
       #    print(" Intent: wert1 ",wert1,"Value: ",wert1_value)
           
       #    ktmp=placechange({0: str(list(slots.keys())[0])},slots)
           
       #elif len(slots) == 2:
       #    print("2 Slots im On Message: ")
       #    wert1 = str(list(slots.keys())[0])
       #    wert1_value = slots[wert1]['value']
       #    wert2 = str(list(slots.keys())[1])
       #    wert2_value = slots[wert2]['value']
           
       #    print(" Intent: wert1  ",wert1,"Value: ",wert1_value)
       #    print(" Intent: wert2 ",wert2,"Value: ",wert2_value)   
           
       #    ktmp=placechange({0: str(list(slots.keys())[0]), 1: str(list(slots.keys())[1])},slots)
           
       #elif len(slots) == 3:
       #    print("3 Slots im On Message: ")
       #    wert1 = str(list(slots.keys())[0])
       #    wert1_value = slots[wert1]['value']
       #    wert2 = str(list(slots.keys())[1])
       #    wert2_value = slots[wert2]['value']
       #    wert3 = str(list(slots.keys())[2])
       #    wert3_value = slots[wert3]['value']
           
       #    print(" Intent: wert1 ",wert1,"Value: ",wert1_value)
       #    print(" Intent: wert2 ",wert2,"Value: ",wert2_value)
       #    print(" Intent: wert3 ",wert3,"Value: ",wert3_value)

       #    ktmp=placechange({0: str(list(slots.keys())[0]), 1: str(list(slots.keys())[1]), 2: str(list(slots.keys())[2])},slots)
           
       #elif len(slots) == 4:
       #    print("4 Slots im On Message: ")
       #    wert1 = str(list(slots.keys())[0])
       #    wert1_value = slots[wert1]['value']
       #    wert2 = str(list(slots.keys())[1])
       #    wert2_value = slots[wert2]['value']
       #   wert3 = str(list(slots.keys())[2])
       #    wert3_value = slots[wert3]['value']
       #    wert4 = str(list(slots.keys())[3])
       #    wert4_value = slots[wert4]['value']
       #    print(" Intent: wert1 ",wert1,"Value: ",wert1_value)
       #    print(" Intent: wert2 ",wert2,"Value: ",wert2_value)
       #    print(" Intent: wert3 ",wert3,"Value: ",wert3_value)
       #    print(" Intent: wert4 ",wert4,"Value: ",wert4_value)

       #   ktmp=placechange({0: str(list(slots.keys())[0]), 1: str(list(slots.keys())[1]), 2: str(list(slots.keys())[2]),3: str(list(slots.keys())[3])},slots)
       try:
           print("Im Try  reaktion.py on_message() ")
        #   print("Ktemp: ",ktmp)
           print(" ")
           kt=globals()[KT]
           seite
           aktion(kt,seite,speed,wenig,intentname,wert1,wert1_value,wert2,wert2_value,wert3,wert3_value,wert4,wert4_value)
       except Exception as e:
           print(e)
    else:
        pixel_ring.listen()


def aktion(kttmp,seitetmp,speedtmp,wenigtmp,intenttmp,wert1,wert1_value,wert2,wert2_value,wert3,wert3_value,wert4,wert4_value):
    print(" ")
    print("IM aktion Modul: reaktion.py|",intenttmp)
# Einzelne Bewegungen    
    if intenttmp == 'senken':
         print("senken: reaktion.py aktion()")
         print("wert1: ",wert1,wert1_value,"wert2: ",wert2,wert2_value,"wert3: ",wert3,wert3_value,"wert4: ",wert4,wert4_value)
         print("KT: ",kt,"Seite: ",seite,"Speed: ",speed,"wenig: ",wenig)
         SBEW.senke(kt,seite,speed,wenig)
         
    elif intenttmp == 'heben':
         print("heben: reaktion.py aktion()")
         print("KT: ",kt,"Seite: ",seite,"Speed: ",speed,"wenig: ",wenig)
         SBEW.hebe(kt,seite,speed,wenig)
         
    elif intenttmp == 'drehen':
         print("drehen: reaktion.py aktion()") 
         print("KT: ",kt,"Seite: ",seite,"Speed: ",speed,"wenig: ",wenig)     
         SBEW.drehe(kt,seite,speed,wenig)
         
    elif intenttmp == 'oeffnen':
         print("oeffnen: reaktion.py aktion()") 
         print("KT: ",kt,"Seite: ",seite,"Speed: ",speed,"wenig: ",wenig) 
         SBEW.oeffne(kt,seite,speed,wenig)
        
    elif intenttmp ==  'schliessen':
         print("schliessen: reaktion.py aktion()") 
         print("KT: ",kt,"Seite: ",seite,"Speed: ",speed,"wenig: ",wenig) 
         SBEW.schliesse(kt,seite,speed,wenig) 
        
# komplexe Bewegungen
    elif intenttmp == 'zeigen':
         print("drehen: reaktion.py aktion()") 
         print("KT: ",kt,"Seite: ",seite,"Speed: ",speed,"wenig: ",wenig) 
         CBEW.zeigen(kt,seite,speed,wenig)
               
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
        SM.sprueche(wert1,wert1_value,wert2,wert2_value,wert3,wert3_value)
        
        
    elif intenttmp == 'Uhrzeit':
        print("Hier geht dier Uhrzeit los: in reaktion.py")
        UHR.uhrzeit(wert1,wert1_value,wert2,wert2_value)
        
    elif intenttmp == 'wetter':
        print("Hier geht das Wetter los: in reaktion.py")
        MY.wetter(wert1,wert1_value,wert2,wert2_value)
        
    elif intenttmp == 'wecker':
        print("Hier geht der Wecker los: in reaktion.py")
        print(" Intent wert1: ",wert1,"Value: ",wert1_value)
        print(" Intent wert2: ",wert2,"Value: ",wert2_value)
        print(" Intent wert3: ",wert3,"Value: ",wert3_value)
        
    elif intenttmp == 'Wohlbefinden':
        
        print("Hier ist das Wohlbefinden: in reaktion.py")
        print(" Intent wert1: ",wert1,"Value: ",wert1_value)
        print(" Intent wert2: ",wert2,"Value: ",wert2_value)
        
        sprache = "Das habe ich nicht verstanden" ## Falls die Funktion einen Wert hat den die IF-clause nicht kennt
                
        temp= MY.wohlbefinden() 
        
        Maxram = MY.getRAMinfo()[0]+ " GigaByte "
        Freeram = MY.getRAMinfo()[1]+ " GigaByte "

        
        if wert1 == "CPUHEAT":
           sprache = "Mir geht es gut . Die Temperatur des Prozessors beträgt "+str(temp)+" Grad. Und das ist innerhalb der normalen Parameter"
           
        elif wert1 == "SPEICHER":
            sprache = "Der Speicher beträgt "+Maxram+ ". Und davon sind "+Freeram+" frei" 
              
        elif wert1 == "KOMPLETHEALTH":
            sprache = "Mir geht es gut. Die Temperatur des Prozessors beträgt "+str(temp)+" Grad . Und das ist innerhalb der normalen Parameter Der Speicher beträgt "+Maxram+ " und davon sind "+Freeram+" frei"
            
        elif wert1 ==   "WASGEHT":
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




mqtt = mqtt.Client() 
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect('192.168.5.71', 1883) 
mqtt.loop_forever()
