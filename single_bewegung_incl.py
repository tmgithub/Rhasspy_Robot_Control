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
import Servo_Include as SI
import mylib as MY
import smalltalk_incl as SM

from datetime import datetime, timedelta
import calendar
import augen as AUGE
from gpiozero import LED
from pixel_ring import pixel_ring
import kopf as KOPF
import sateliten_arm_hand_finger as SAHF


from rhasspyhermes.wake import HotwordDetected

import globs

import threading

# Funtion zum heben           
def hebe(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp):
    
        print("heben:  single_bewegung_incl.py hebe()")
        print("####",kttmp,subkttmp,seitetmp,speedtmp,wenigtmp)
# Abfrage mit welcher Geschwindigkeit sich das Körperteil bewegen soll       
        if speedtmp == 'slow' or speedtmp == 'SLOW':
           speed_slow = 'True'
        else:
           speed_slow = 'False'
# Zum debuggen Ausgabe der Werte  aktivieren         
        #print("Bin im heben modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)   

        if kttmp == 'Kopf':                  # Der Kopf wird angesprochen
            sprache="Ich soll meinen Kopf "+wenigtmp+ " heben "+speedtmp
            MY.sprachausgabe('"%s"' %sprache)
            
            KOPF.kopf_heben(kttmp,seitetmp,speed_slow,wenigtmp)

        elif  kttmp == "Arm":
            
            #if seitetmp[:2] =="re" or seitetmp[:2] == "li":
                
            sprache="Ich soll meinen "+seitetmp+" Arm "+speedtmp+" "+wenigtmp + " heben"
            MY.sprachausgabe('"%s"' %sprache)
               
            SAHF.arm_heben(kttmp,seitetmp,speed_slow,wenigtmp)
            
        elif  kttmp == "Arme":    # Die Arme werden angesprochen 
            
            sprache="Ich soll meine "+seitetmp+"n Arme "+wenigtmp + " heben "+speedtmp
            MY.sprachausgabe('"%s"' %sprache)
            
            SAHF.arm_heben(kttmp,seitetmp,speed_slow,wenigtmp)
              
        elif kttmp == "Bein":

            sprache="Ich soll mein "+seitetmp+" Bein "+speedtmp+" "+wenigtmp + " heben"
            MY.sprachausgabe('"%s"' %sprache)
                      
            MY.bein_heben(kttmp,seitetmp,speed_slow,wenigtmp)
            
        elif  kttmp == "Beine":    # Die Beine werden angesprochen 
            
            sprache="Ich soll meine "+seitetmp+"n Beine "+wenigtmp + " heben "+speedtmp+". Aber das geht nicht dann falle ich um."
            MY.sprachausgabe('"%s"' %sprache)
            
            #MY.bein_heben(kttmp,seitetmp,speed_slow,wenigtmp)      

# Funtion zum heben           
def senke(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp):
        print("senken: single_bewegung_incl.py senke()") 
        print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)       
        if speedtmp == 'slow' or speedtmp == 'SLOW':
           speed_slow = 'True'
        else:
           speed_slow = 'False'
# Zum debuggen Ausgabe der Werte  aktivieren         
        #print("Bin im heben modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)   


        if kttmp == 'kopf' or kttmp == 'Kopf':                  # Der Kopf wird angesprochen
            sprache="Ich soll meinen Kopf "+speedtmp + " senken"
            MY.sprachausgabe('"%s"' %sprache)
            MY.kopf_senken(kttmp,seitetmp,speed_slow,wenigtmp)

        elif kttmp == "arm" or kttmp == "Arm":
            print("KT: ",kttmp)
            sprache="Ich soll meinen "+seitetmp+" Arm "+speedtmp + " senken"
            MY.sprachausgabe('"%s"' %sprache) 
            SAHF.arm_senken(kttmp,seitetmp,speed_slow,wenigtmp)
            
        elif kttmp == "arme" or kttmp == "Arme":    # Die Arme werden angesprochen 
            print("KT: ",kttmp)
            sprache="Ich soll meine Arme "+speedtmp + " senken"
            MY.sprachausgabe('"%s"' %sprache) 
            SAHF.arm_senken(kttmp,seitetmp,speed_slow,wenigtmp)
              
            #print(kttmp, "-", seitetmp, "-", speed_slow)
        elif kttmp == "bein" or kttmp == "Bein" or kttmp == "beine" or kttmp == "Beine":

            MY.bein_senken(kttmp,seitetmp,speed_slow,wenigtmp)
            
# Funtion zum drehen           
def drehe(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp):
        print("drehen:  single_bewegung_incl.py drehe()")
# Abfrage mit welcher Geschwindigkeit sich das Körperteil bewegen soll       
        if speedtmp == 'slow' or speedtmp == 'SLOW':
           speed_slow = 'True'
        else:
           speed_slow = 'False'
# Zum debuggen Ausgabe der Werte  aktivieren         
        #print("Bin im drehen modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)   

        if kttmp == 'kopf' or kttmp == 'Kopf':                  # Der Kopf wird angesprochen
#            sprache="Ich soll meinen Kopf "+real_speed + "nach" + real_seite +" drehen"
 #           MY.sprachausgabe('"%s"' %sprache)
            KOPF.kopf_drehen(kttmp,seitetmp,speed_slow,wenigtmp)

        elif kttmp == "arm" or kttmp == "Arm" or kttmp == "arme" or kttmp == "Arme":    # Die Arme werden angesprochen 
            print("KT: ",kttmp)
            sprache="Ich soll meine Arm "+real_speed + "nach" + real_seite +" drehen"
            MY.sprachausgabe('"%s"' %sprache)
            SAHF.arm_drehen(kttmp,seitetmp,speed_slow,wenigtmp)
              
            #print(kttmp, "-", seitetmp, "-", speed_slow)
        elif kttmp == "Bein" or kttmp == "beine" or kttmp == "Beine":

            MY.bein_heben(kttmp,seitetmp,speed_slow,wenigtmp)

def oeffne(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp):
        print("öffnen:  single_bewegung_incl.py oeffne()")
# Abfrage mit welcher Geschwindigkeit sich das Körperteil bewegen soll       
        if speedtmp == 'slow' or speedtmp == 'SLOW':
           speed_slow = 'True'
        else:
           speed_slow = 'False'
# Zum debuggen Ausgabe der Werte  aktivieren         
        print("Bin im oeffnen Modul: ",kttmp,seitetmp,speedtmp,wenigtmp)   

        if subkttmp == "Mund":
            print("SUBKT: ",subkttmp)
            sprache="Ich soll meinen Mund "+speedtmp + " oeffnen"
            MY.sprachausgabe('"%s"' %sprache) 
            SAHF.arm_senken(kttmp,seitetmp,speed_slow,wenigtmp)

        elif subkttmp == "Auge":    # Die Augen werden angesprochen 
            print("SUBKT: ",subkttmp)
            sprache="Ich soll mein "+seitetmp+"s Auge "+speedtmp + " oeffnen"
            print(sprache)
            MY.sprachausgabe('"%s"' %sprache) 
            AUGE.auge_oeffnen(kttmp,subkttmp,seitetmp,speed_slow,wenigtmp)
            #MY.arm_senken(kttmp,seitetmp,speed_slow,wenigtmp)
            #
        elif subkttmp == "Augen":    # Die Augen werden angesprochen 
            print("SUBKT: ",subkttmp)
            sprache="Ich soll meine Augen "+speedtmp + " oeffnen"
            MY.sprachausgabe('"%s"' %sprache) 
            AUGE.auge_oeffnen(kttmp,subkttmp,seitetmp,speed_slow,wenigtmp)
            
        elif subkttmp == "Fäuste" or kttmp == "Hände":
            print("SUBKT: ",subkttmp)
            sprache="Ich soll meine "+kttmp+" "+speedtmp + " oeffnen"
            MY.sprachausgabe('"%s"' %sprache)



def schliesse(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp):
        print("schliesse:  single_bewegung_incl.py schliesse()")
        print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)
        print(" ")
# Abfrage mit welcher Geschwindigkeit sich das Körperteil bewegen soll       
        if speedtmp == 'slow' or speedtmp == 'SLOW':
           speed_slow = 'True'
        else:
           speed_slow = 'False'
# Zum debuggen Ausgabe der Werte  aktivieren         
        #print("Bin im schliessen Modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)   

        if  subkttmp == "Mund":
            print("SUBKT: ",subkttmp)
            sprache="Ich soll meinen Mund "+speedtmp + " schliessen"
            MY.sprachausgabe('"%s"' %sprache) 
            #SAHF.arm_senken(kttmp,seitetmp,speed_slow,wenigtmp)
            
        elif subkttmp == "Auge":    # Die Augen werden angesprochen 
            print("SUBKT: ",subkttmp)
            sprache="Ich soll mein "+seitetmp+"s Auge "+speedtmp + " schliessen"
            print(sprache)
            MY.sprachausgabe('"%s"' %sprache) 
            AUGE.auge_schliessen(kttmp,subkttmp,seitetmp,speed_slow,wenigtmp)
        elif kttmp == "Augen":    # Die Augen werden angesprochen 
            print("SUBKT: ",subkttmp)
            sprache="Ich soll meine Augen "+seitetmp + " schliessen"
            MY.sprachausgabe('"%s"' %sprache) 
            AUGE.auge_schliessen(kttmp,subkttmp,seitetmp,speed_slow,wenigtmp)

