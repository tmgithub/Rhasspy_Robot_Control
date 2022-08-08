#!/usr/bin/env python3
# encoding: utf-8

## Hauptprogramm zur Steuerung der Servos durch Spracheingabe

from __future__ import print_function
from __future__ import division
from random import randint
import os
import glob
import time
import constant as co
import sys
import Servo_Include as SI

from datetime import datetime, timedelta
import calendar

import globs

import threading

def zeigen(kttmp,subkttmp,seitetmp,speedtmp,wenigtmp,myslots,intenttmp,subanz,subaktion):
        print("Aktion zeigen:  complex_bewegung_incl.py zeigen() ")
        print("KT: ",kttmp,"SUBKT: ",subkttmp,"Intent: ",intenttmp,"Seite: ",seitetmp,"ANZAHL: ",subanz,"Speed: ",speedtmp,"wenig: ",wenigtmp,"aktion: ",subaktion)
        print(" ")
# Abfrage mit welcher Geschwindigkeit sich das Körperteil bewegen soll       
        if speedtmp == 'slow' or speedtmp == 'SLOW':
           speed_slow = 'True'
        else:
           speed_slow = 'False'
# Zum debuggen Ausgabe der Werte  aktivieren         
        #print("Bin im heben modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)   

        print("Seitetmp: ",seitetmp[0:2])
        print("Anzahl: ",subanz)
        if  subkttmp == 'Faust' and seitetmp =="":               # Der Kopf wird angesprochen
            pass
            
        elif subkttmp == "Fäuste":
            pass

            
        elif subkttmp == 'Faust':              # Der Kopf wird angesprochen

             SI.move_servo(co.zfinger, co.zfinger_krumm, co.fast)
             SI.write_servopos(co.zfinger, co.zfinger_krumm)
    
             SI.move_servo(co.mfinger, co.mfinger_gerade, co.fast)
             SI.write_servopos(co.mfinger, co.mfinger_krumm)
    
             SI.move_servo(co.rfinger, co.rfinger_krumm, co.fast)
             SI.write_servopos(co.rfinger, co.rfinger_krumm)
             
             SI.move_servo(co.kfinger, co.kfinger_krumm, co.fast)
             SI.write_servopos(co.kfinger,co.kfinger_krumm)

        elif subkttmp == 'Zeigefinger':              # Die Hand wird angesprochen
             SI.move_servo(co.zfinger, co.zfinger_gerade, co.fast)
             SI.write_servopos(co.zfinger, co.zfinger_gerade)
    
             SI.move_servo(co.mfinger, co.mfinger_krumm, co.fast)
             SI.write_servopos(co.mfinger, co.mfinger_krumm)
    
             SI.move_servo(co.rfinger, co.rfinger_krumm, co.fast)
             SI.write_servopos(co.rfinger, co.rfinger_krumm)
    
             SI.move_servo(co.kfinger, co.kfinger_krumm, co.fast)
             SI.write_servopos(co.kfinger,co.kfinger_krumm)

        elif subkttmp == 'Mittelfinger':              # Die Hand wird angesprochen

             SI.move_servo(co.zfinger, co.zfinger_krumm, co.fast)
             SI.write_servopos(co.zfinger, co.zfinger_krumm)
    
             SI.move_servo(co.mfinger, co.mfinger_gerade, co.fast)
             SI.write_servopos(co.mfinger, co.mfinger_gerade)
    
             SI.move_servo(co.rfinger, co.rfinger_krumm, co.fast)
             SI.write_servopos(co.rfinger, co.rfinger_krumm)
    
             SI.move_servo(co.kfinger, co.kfinger_krumm, co.fast)
             SI.write_servopos(co.kfinger,co.kfinger_krumm)
             
        elif subkttmp == 'Hand' and subaktion[0:2] == "wi":
             print("Tadah")              # Die Hand wird angesprochen
             SI.move_servo(co.handwinken, 50, co.slow)
             SI.write_servopos(co.handwinken, 50)
             time.sleep(2)
             SI.move_servo(co.handwinken, 150, co.slow)
             SI.write_servopos(co.handwinken, 150)
             SI.move_servo(co.handwinken, co.servo_middle, co.slow)
             SI.write_servopos(co.handwinken, co.servo_middle)
    
             #SI.move_servo(co.mfinger, co.mfinger_gerade, co.fast)
             #SI.write_servopos(co.mfinger, co.mfinger_gerade)
    
             #SI.move_servo(co.rfinger, co.rfinger_krumm, co.fast)
             #SI.write_servopos(co.rfinger, co.rfinger_krumm)
    
             #SI.move_servo(co.kfinger, co.kfinger_krumm, co.fast)
             #SI.write_servopos(co.kfinger,co.kfinger_krumm)

        elif subkttmp == 'Finger': 
             print("Jawohl: ")
             print("subanz: ",type(subanz))
             if subanz == "1":
                 SI.move_servo(co.zfinger, co.zfinger_gerade, co.fast)
                 SI.write_servopos(co.zfinger, co.zfinger_gerade)
    
                 SI.move_servo(co.mfinger, co.mfinger_krumm, co.fast)
                 SI.write_servopos(co.mfinger, co.mfinger_krumm)
    
                 SI.move_servo(co.rfinger, co.rfinger_krumm, co.fast)
                 SI.write_servopos(co.rfinger, co.rfinger_krumm)

                 SI.move_servo(co.kfinger, co.kfinger_krumm, co.fast)
                 SI.write_servopos(co.kfinger,co.kfinger_krumm)
                 
             elif subanz == "2":
                 SI.move_servo(co.zfinger, co.zfinger_gerade, co.fast)
                 SI.write_servopos(co.zfinger, co.zfinger_gerade)
                 
                 SI.move_servo(co.mfinger, co.mfinger_gerade, co.fast)
                 SI.write_servopos(co.mfinger, co.mfinger_gerade)

    
                 SI.move_servo(co.rfinger, co.rfinger_krumm, co.fast)
                 SI.write_servopos(co.rfinger, co.rfinger_krumm)
    
                 SI.move_servo(co.kfinger, co.kfinger_krumm, co.fast)
                 SI.write_servopos(co.kfinger,co.kfinger_krumm)                 
                 
             elif subanz == "3":
                 SI.move_servo(co.zfinger, co.zfinger_gerade, co.fast)
                 SI.write_servopos(co.zfinger, co.zfinger_gerade)
                 
                 SI.move_servo(co.mfinger, co.mfinger_gerade, co.fast)
                 SI.write_servopos(co.mfinger, co.mfinger_gerade)
    
                 SI.move_servo(co.rfinger, co.rfinger_gerade, co.fast)
                 SI.write_servopos(co.rfinger, co.rfinger_gerade)

    
                 SI.move_servo(co.kfinger, co.kfinger_krumm, co.fast)
                 SI.write_servopos(co.kfinger,co.kfinger_krumm)
                 
             elif subanz == "4":
                 print("JAJA")
                 SI.move_servo(co.zfinger, co.zfinger_gerade, co.fast)
                 SI.write_servopos(co.zfinger, co.zfinger_gerade)
                 
                 SI.move_servo(co.mfinger, co.mfinger_gerade, co.fast)
                 SI.write_servopos(co.mfinger, co.mfinger_gerade)
    
                 SI.move_servo(co.rfinger, co.rfinger_gerade, co.fast)
                 SI.write_servopos(co.rfinger, co.rfinger_gerade) 
                   
                 SI.move_servo(co.kfinger, co.kfinger_gerade, co.fast)
                 SI.write_servopos(co.kfinger,co.kfinger_gerade)

