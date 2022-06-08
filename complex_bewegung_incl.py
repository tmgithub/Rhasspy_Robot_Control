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

from rhasspyhermes.wake import HotwordDetected

import globs

import threading

def zeigen(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp):
        print("Aktion zeigen:  complex_bewegung_incl.py zeigen() ")
        print("KT: ",kttmp,"SUBKT: ",subkttmp,"Seite: ",seitetmp,"Speed: ",speedtmp,"wenig: ",wenigtmp)
# Abfrage mit welcher Geschwindigkeit sich das Körperteil bewegen soll       
        if speedtmp == 'slow' or speedtmp == 'SLOW':
           speed_slow = 'True'
        else:
           speed_slow = 'False'
# Zum debuggen Ausgabe der Werte  aktivieren         
        #print("Bin im heben modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)   

        print("Seitetmp: ",seitetmp[0:2])
        if  subkttmp == 'Faust' and seitetmp =="":               # Der Kopf wird angesprochen
            sprache="Ich soll "+speedtmp +" eine "+subkttmp+" machen. Aber ich weiß nicht mit welcher Hand. Bitte wiederhole die Anfrage noch einmal mit der Angabe links oder rechts."
            MY.sprachausgabe('"%s"' %sprache)
            
        elif subkttmp == "Fäuste":

            sprache="Ich soll beide Fäuste "+speedtmp + " ballen."
            MY.sprachausgabe('"%s"' %sprache)
            
        elif subkttmp == 'Faust' and seitetmp[0:2] =="li":               # Der Kopf wird angesprochen
            sprache="Ich soll "+seitetmp+" "+speedtmp +" eine "+subkttmp+" machen. "
            MY.sprachausgabe('"%s"' %sprache)
            
            
        elif subkttmp == 'Faust' and seitetmp[0:2] =="re":               # Der Kopf wird angesprochen
            sprache="Ich soll "+seitetmp+" "+speedtmp +" eine "+subkttmp+" machen. "
            MY.sprachausgabe('"%s"' %sprache)
        