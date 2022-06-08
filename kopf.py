  #!/usr/bin/env python3
# encoding: utf-8
from __future__ import print_function
from __future__ import division
import paho.mqtt.client as mqtt 
import json
from random import randint
import os
import subprocess
import glob
import time
import constant as co
import Servo_Include as SI
import sys
import calendar
import datetime
from datetime import timedelta

import importlib
importlib.reload(sys)
from gpiozero import LED
from pixel_ring import pixel_ring

import requests

import globs
import threading

import mylib as MY


def kopf_drehen(kttmp,seitetmp,speed_slow,wenigtmp):
# Zum debuggen Ausgabe der Werte  aktivieren         
            print("Kopf drehen:  kopf.py kopf_drehen()")
           #print("Bin im heben modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)             
            print("Seitetmp: ",seitetmp[0:2])
            if seitetmp[0:2] == "li":
                sprache="Ich soll den Kopf nach links drehen"
                MY.sprachausgabe('"%s"' %sprache)
                readwert = SI.read_servopos(co.kopfd)      # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                neuwert = co.kopf_links_drehen                          # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                print("ausgelesener Wert: ", readwert,"Konstant: ",co.kopf_links_drehen,"Neuwert: ",neuwert)

                if readwert == co.kopf_links_drehen:
                    #print("Pups")
                    sprache="aber Kopf ist schon ganz links"
                    MY.sprachausgabe('"%s"' %sprache)
                else:
                    #print("Inder Else: ",wenigtmp)
                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        #print("Hier ab: ",wenigtmp)
                        neuwert = readwert + 25
                        #print("Neuwert nach addition. ",neuwert)
                        if neuwert >= co.kopf_links_drehen:
                            neuwert = co.kopf_links_drehen              # Den Wert sicherheitshalber auf den maximalen Wert setzen
                            sprache="aber mein Kopf ist schon ganz links"    
                            MY.sprachausgabe('"%s"' %sprache) 
                            #print("Scheiß_neuwert: ",neuwert)        
                    #print("heb heb", neuwert)    
                    SI.move_servo(co.kopf_drehen,neuwert, speed_slow) 
                   
            elif seitetmp[0:2] == "re":
                sprache="Ich soll den Kopf nach rechts drehen"
                MY.sprachausgabe('"%s"' %sprache)                
                readwert = SI.read_servopos(co.kopf_drehen)         # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                neuwert = co.kopf_rechts_drehen                              # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                #print("ausgelesener Wert: ", readwert)
                
                if readwert == co.kopf_rechts_drehen:
                   sprache="aber mein Kopf ist schon ganz rechts"
                   MY.sprachausgabe('"%s"' %sprache)               
                else:
                     #print("Inder Else: ",wenigtmp)
                    if wenigtmp == 'ab':
                        #print("Hier ab: ",wenigtmp)
                        neuwert = readwert - 25
                        #print("Neuwert nach addition. ",neuwert)
                        if neuwert >= co.arm_heben:
                            neuwert = co.arm_heben
                            sprache="aber Kopf ist schon ganz rechts"    
                            MY.sprachausgabe('"%s"' %sprache)  
                            #print("Scheiß_neuwert: ",neuwert)        
                    #print("heb heb", neuwert)    
                    SI.move_servo(co.kopf_drehen,neuwert, speed_slow)    
                     
               
            elif seitetmp == "mi":
                sprache="Ich soll den Kopf lzur Mitte drehen"
                MY.sprachausgabe('"%s"' %sprache)
                readwert = SI.read_servopos(co.kopf_drehen)        # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                neuwert = co.kopf_neutral
                
                #print("linker ausgelesener Wert: ", links_readwert,"Konstant: ",co.arm_heben)
                #print("rechter ausgelesener Wert: ", rechts_readwert,"Konstant: ",co.arm_heben)

                if readwert == co.kopf_neutral:
                   sprache="mein Kopf zeigt bereits geradeaus"
                   MY.sprachausgabe('"%s"' %sprache)
                else:
                    #print("Inder Else: ",wenigtmp)
                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        
                        #print("Hier beide ab: ",wenigtmp)
                        links_neuwert = links_readwert - 25
                        
                        if neuwert >= co.kopf_neutral:

                            neuwert = co.kopf_neutral
                            rechts_neuwert = co.arm_heben
                            
                            sprache="mein Kopf zeigt schon geradeaus"                              
                            MY.sprachausgabe('"%s"' %sprache)
 
                            #print("Scheiß_neuwert: ",neuwert)        
    
                    #print("Hier sollten sich die Arme bewegen: ", rechts_neuwert, links_neuwert)
                    SI.move_servo(co.kopf_drehen,neuwert, speed_slow) 


def kopf_heben(kttmp,seitetmp,speed_slow,wenigtmp):
    # Die letzte Position des Servos auslesen            
            readwert = SI.read_servopos(co.kopf_heben)
            neuwert = co.kopf_heben                             # Wichtig falls die wenigtempschleife nicht durchlaufen wird
            
            if seitetmp == "be":                                # Wenn die Neutralstellung gewuenscht wird
                
                if readwert == co.kopf_neutral:                 #schauen ob der Neutralwert bereits erreicht ist
                    sprache="aber ich schaue schon geradeaus "    
                    MY.sprachausgabe('"%s"' %sprache)
                else:                                           # Den Kopf in die Mittelstellung was die Nickposition betrifft bringen
                    SI.move_servo(co.kopf_heben,co.kopf_neutral, speed_slow)

            else:                                               # wenn das heben erwünscht ist

                if readwert == co.kopf_heben:                   # schauen ob der Maximalwert bereits erreicht ist
                    sprache="aber mein Kopf ist schon oben"    
                    MY.sprachausgabe('"%s"' %sprache)   
                else:
                    if wenigtmp == 'ab':
                        neuwert = readwert - 25
                        if neuwert <= co.kopf_heben:
                            neuwert = co.kopf_heben 
                            sprache="aber mein Kopf ist schon oben"    
                            MY.sprachausgabe('"%s"' %sprache)
                                        
                    SI.move_servo(co.kopfh,neuwert,speed_slow)
                    
def kopf_senken(kttmp,seitetmp,speed_slow,wenigtmp):
    # Die letzte Position des Servos auslesen            
            readwert = SI.read_servopos(co.kopf_heben)
            neuwert = co.kopf_senken                             # Wichtig falls die wenigtempschleife nicht durchlaufen wird
            
            if seitetmp == "be":                                # Wenn die Neutralstellung gewuenscht wird
                
                if readwert == co.kopf_neutral:                 #schauen ob der Neutralwert bereits erreicht ist
                    sprache="aber ich schaue schon geradeaus "    
                    MY.sprachausgabe('"%s"' %sprache)
                else:                                           # Den Kopf in die Mittelstellung was die Nickposition betrifft bringen
                    SI.move_servo(co.kopf_heben,co.kopf_neutral, speed_slow)

            else:                                               # wenn das heben erwünscht ist

                if readwert == co.kopf_senken:                   # schauen ob der Maximalwert bereits erreicht ist
                    sprache="aber mein Kopf ist schon unten"    
                    MY.sprachausgabe('"%s"' %sprache)   
                else:
                    if wenigtmp == 'ab':
                        neuwert = readwert + 25
                        if neuwert <= co.kopf_senken:
                            neuwert = co.kopf_senken 
                            sprache="aber mein Kopf ist schon unten"    
                            MY.sprachausgabe('"%s"' %sprache)
                                        
                    SI.move_servo(co.kopf_heben,neuwert,speed_slow)
