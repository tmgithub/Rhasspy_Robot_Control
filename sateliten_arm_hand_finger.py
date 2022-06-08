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


def arm_senken(kttmp,seitetmp,speed_slow,wenigtmp):

            print("Arm senken :  sateliten_arm_hand_finger.py arm_senken()")
    
    
# Zum debuggen Ausgabe der Werte  aktivieren         
            print("Bin im senken modul: ",kttmp,seitetmp,wenigtmp,speed_slow)             

            if seitetmp[0:2] == "li":

                readwert = SI.read_servopos(co.linken_arm) 
                #print("links: ",readwert)     # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                neuwert = co.arm_senken                          # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                print("ausgelesener Wert: ", readwert,"Konstant: ",co.arm_senken,"Neuwert: ",neuwert)

                if readwert == co.arm_senken:
                    #print("Pups")
                    sprache="aber mein linker Arm ist schon ganz unten"
                    MY.sprachausgabe('"%s"' %sprache)
                else:
                    #print("Inder Else: ",wenigtmp)
                    if wenigtmp == 'AB':                        # wenn nur eine kleine Bewegung gewünscht wird
                        #print("Hier ab: ",wenigtmp)
                        neuwert = readwert - 25
                        #print("Neuwert nach addition. ",neuwert)
                        if neuwert >= co.arm_senken:
                            neuwert = co.arm_senken              # Den Wert sicherheitshalber auf den maximalen Wert setzen
                            sprache="aber mein linker Arm ist schon unten"    
                            sprachausgabe('"%s"' %sprache) 
                            #print("Scheiß_neuwert: ",neuwert)        
                    #print("heb heb", neuwert)    

 
                    kt_payload=json.dumps({'servoID':co.linken_arm,'servostepvalue': neuwert,'speed': speed_slow,'step_value': wenigtmp,'siteId': 'default', 'modelId': 'default'})
                    MY.publish("hermes/linkerArm",kt_payload)
                    #SI.move_servo(co.linken_arm,neuwert, speed_slow) 
                   
            elif seitetmp == "re":
                readwert = SI.read_servopos(co.rechten_arm)
                #print("Read rechter arm: ",readwert,co.rechten_arm)         # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                neuwert = co.arm_senken                              # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                #print("ausgelesener Wert: ", readwert)
                print("ausgelesener Wert: ", readwert,"Konstant: ",co.arm_senken,"Neuwert: ",neuwert,"Wenig: ",wenigtmp)
                
                if readwert == co.arm_senken:
                   sprache="aber mein rechter Arm ist schon ganz unten"
                   sprachausgabe('"%s"' %sprache)               
                else:
                     #print("Inder Else: ",wenigtmp)
                    if wenigtmp == 'ab':
                        #print("Hier ab: ",wenigtmp)
                        neuwert = readwert - 25
                        #print("Neuwert nach addition. ",neuwert)
                        if neuwert >= co.arm_senken:
                            neuwert = co.arm_senken 
                            #print("Scheiß_neuwert: ",neuwert)        
                    #print("heb heb", neuwert)    
                    kt_payload=json.dumps({'servoID':co.rechten_arm,'servostepvalue': neuwert,'speed': speed_slow,'step_value': wenigtmp,'siteId': 'default', 'modelId': 'default'})
                    MY.publish("hermes/rechterArm",kt_payload)
                    #SI.move_servo(co.rechten_arm,neuwert, speed_slow)    
                     
               
            elif seitetmp == "be":
                links_readwert = SI.read_servopos(co.linken_arm)        # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                rechts_readwert = SI.read_servopos(co.rechten_arm)      # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                links_neuwert = co.arm_senken
                rechts_neuwert = co.arm_senken
                print("ausgfrom datetime import datetime, timedeltaelesener Wert: ", readwert,"Konstant: ",co.arm_senken,"Neuwert: ",neuwert)
                #print("linker ausgelesener Wert: ", links_readwert,"Konstant: ",co.arm_heben)
                #print("rechter ausgelesener Wert: ", rechts_readwert,"Konstant: ",co.arm_heben)

                if links_readwert == co.arm_senken and rechts_readwert == co.arm_senken:
                   sprache="aber meine Arme sind schon ganz unten"
                   sprachausgabe('"%s"' %sprache)
                else:
                    #print("Inder Else: ",wenigtmp)
                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        
                        #print("Hier beide ab: ",wenigtmp)
                        links_neuwert = links_readwert - 25
                        rechts_neuwert = rechts_readwert - 25
                        #print("Linkerneuwert nach addition. ",links_neuwert)
                        #print("Rechterneuwert nach addition. ",rechts_neuwert)
                        
                        if links_neuwert >= co.arm_senken and rechts_neuwert >= co.arm_senken:

                            links_neuwert = co.arm_senken
                            rechts_neuwert = co.arm_senken
                            
                            sprache="aber meine Arme sind schon oben"                              
                            sprachausgabe('"%s"' %sprache)
 
                            #print("Scheiß_neuwert: ",neuwert)        
    
                    #print("Hier sollten sich die Arme bewegen: ", rechts_neuwert, links_neuwert)
                    kt_payload=json.dumps({'servoID':co.linken_arm,'servostepvalue': neuwert,'speed': speed_slow,'step_value': wenigtmp,'siteId': 'default', 'modelId': 'default'})
                    MY.publish("hermes/beideArme",kt_payload)
                   # SI.move_servo(co.rechten_arm,rechts_neuwert, speed_slow) 
                   # SI.move_servo(co.linken_arm,links_neuwert, speed_slow)


            
def arm_heben(kttmp,seitetmp,speed_slow,wenigtmp):
    
    
# Zum debuggen Ausgabe der Werte  aktivieren         
           #print("Bin im heben modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)             

            if seitetmp[:2] == "li":

                readwert = SI.read_servopos(co.linken_arm)      # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                neuwert = co.arm_heben                          # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                print("ausgelesener Wert: ", readwert,"Konstant: ",co.arm_heben,"Neuwert: ",neuwert)

                if readwert == co.arm_heben:
                    #print("Pups")
                    sprache="aber mein linker Arm ist schon ganz oben"
                    sprachausgabe('"%s"' %sprache)
                else:
                    #print("Inder Else: ",wenigtmp)
                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        #print("Hier ab: ",wenigtmp)
                        neuwert = readwert + 25
                        #print("Neuwert nach addition. ",neuwert)
                        if neuwert >= co.arm_heben:
                            neuwert = co.arm_heben              # Den Wert sicherheitshalber auf den maximalen Wert setzen
                            sprache="aber mein linker Arm ist schon oben"    
                            sprachausgabe('"%s"' %sprache) 
                            #print("Scheiß_neuwert: ",neuwert)        
                    #print("heb heb", neuwert)    
                    SI.move_servo(co.linken_arm,neuwert, speed_slow) 
                   
            elif seitetmp[:2] == "re":
                readwert = SI.read_servopos(co.rechten_arm)         # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                neuwert = co.arm_heben                              # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                #print("ausgelesener Wert: ", readwert)
                print("ausgelesener Wert: ", readwert,"Konstant: ",co.arm_heben,"Neuwert: ",neuwert)
                
                if readwert == co.arm_heben:
                   sprache="aber mein rechter Arm ist schon ganz oben"
                   sprachausgabe('"%s"' %sprache)               
                else:
                     #print("Inder Else: ",wenigtmp)
                    if wenigtmp == 'ab':
                        #print("Hier ab: ",wenigtmp)
                        neuwert = readwert + 25
                        #print("Neuwert nach addition. ",neuwert)
                        if neuwert >= co.arm_heben:
                            neuwert = co.arm_heben 
                            #print("Scheiß_neuwert: ",neuwert)        
                    #print("heb heb", neuwert)    
                    SI.move_servo(co.rechten_arm,neuwert, speed_slow)    
                     
               
            elif seitetmp[:2] == "be":
                links_readwert = SI.read_servopos(co.linken_arm)        # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                rechts_readwert = SI.read_servopos(co.rechten_arm)      # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                links_neuwert = co.arm_heben
                rechts_neuwert = co.arm_heben
                
                #print("linker ausgelesener Wert: ", links_readwert,"Konstant: ",co.arm_heben)
                #print("rechter ausgelesener Wert: ", rechts_readwert,"Konstant: ",co.arm_heben)
                print("ausgelesener Wert: ", links_readwert,"Konstant: ",co.arm_heben,"Neuwert: ",links_neuwert)
                print("ausgelesener Wert: ", rechts_readwert,"Konstant: ",co.arm_heben,"Neuwert: ",rechts_neuwert)

                if links_readwert == co.arm_heben and rechts_readwert == co.arm_heben:
                   sprache="aber meine Arme sind schon ganz oben"
                   sprachausgabe('"%s"' %sprache)
                else:
                    #print("Inder Else: ",wenigtmp)
                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        
                        #print("Hier beide ab: ",wenigtmp)
                        links_neuwert = links_readwert + 25
                        rechts_neuwert = rechts_readwert + 25
                        #print("Linkerneuwert nach addition. ",links_neuwert)
                        #print("Rechterneuwert nach addition. ",rechts_neuwert)
                        
                        if links_neuwert >= co.arm_heben and rechts_neuwert >= co.arm_heben:

                            links_neuwert = co.arm_heben
                            rechts_neuwert = co.arm_heben
                            
                            sprache="aber meine Arme sind schon oben"                              
                            sprachausgabe('"%s"' %sprache)
 
                            #print("Scheiß_neuwert: ",neuwert)        
    
                    #print("Hier sollten sich die Arme bewegen: ", rechts_neuwert, links_neuwert)
                    SI.move_servo(co.rechten_arm,rechts_neuwert, speed_slow) 
                    SI.move_servo(co.linken_arm,links_neuwert, speed_slow)
    
#def auge_schliessen(kttmp,seitetmp,speed_slow,wenigtmp):
            #print("Servo Nummern: ",co.linken_arm, co.rechten_arm)
    
    
# Zum debuggen Ausgabe der Werte  aktivieren         
           #print("Bin im heben modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)             

#            if seitetmp == "li":
                #print("Bin da")

#                readwert = SI.read_servopos(co.linkes_lid) 
                #print("links: ",readwert)     # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
#                neuwert = co.li_auge_schliessen                          # Wichtig falls die wenigtempschleife nicht durchlaufen wird
#                print("ausgelesener Wert: ", readwert,"Konstant: ",co.li_auge_schliessen,"Neuwert: ",neuwert)

#                if readwert == co.li_auge_schliessen:
                    #print("Pups")
#                    sprache="aber mein linkes Auge ist schon zu"
#                    sprachausgabe('"%s"' %sprache)
#                else:
                    #print("Inder Else: ",wenigtmp)
#                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        #print("Hier ab: ",wenigtmp)
#                        neuwert = readwert - 25
                        #print("Neuwert nach addition. ",neuwert)
#                        if neuwert >= co.li_auge_schliessen:
#                            neuwert = co.li_auge_schliessen              # Den Wert sicherheitshalber auf den maximalen Wert setzen
#                            sprache="aber mein linkes Auge ist schon zu"    
#                            sprachausgabe('"%s"' %sprache) 
                            #print("Scheiß_neuwert: ",neuwert)        
                    #print("heb heb", neuwert)    
#                    SI.move_servo(co.linkes_lid,neuwert, speed_slow) 
                   
#            elif seitetmp == "re":
#                readwert = SI.read_servopos(co.rechtes_lid)
                #print("Read rechter arm: ",readwert,co.rechten_arm)         # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
#                neuwert = co.re_auge_schliessen                              # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                #print("ausgelesener Wert: ", readwert)
#                print("ausgelesener Wert: ", readwert,"Konstant: ",co.re_auge_schliessen,"Neuwert: ",neuwert)
                
#                if readwert == co.re_auge_schliessen:
#                   print("Wogenau")
#                   sprache="aber mein rechtes Auge ist schon zu"
#                   sprachausgabe('"%s"' %sprache)               
#                else:
#                    print("Inder Else: ",wenigtmp)
#                    if wenigtmp == 'ab':
                        #print("Hier ab: ",wenigtmp)
#                        neuwert = readwert - 25
                        #print("Neuwert nach addition. ",neuwert)
#                        if neuwert >= co.re_auge_schliessen:
#                            neuwert = co.re_auge_schliessen 
                            #print("Scheiß_neuwert: ",neuwert)        
#                    print("heb heb", neuwert)    
#                    SI.move_servo(co.rechtes_lid,neuwert, speed_slow)    
                     
               
#            elif seitetmp == "be":
                #print("Bis hier2")
#                print(co.linkes_lid)
#                print(co.rechtes_lid)
                #try:
#                links_readwert = SI.read_servopos(co.linkes_lid)        # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
#                rechts_readwert = SI.read_servopos(co.rechtes_lid)      # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                #except Exception as e:
                #    print(e)
                    
#                links_neuwert = co.li_auge_schliessen
#                rechts_neuwert = co.li_auge_schliessen
#                print("ausgfrom datetime import datetime, timedeltaelesener Wert: ", rechts_readwert," ", links_readwert, "Konstant: ",co.li_auge_schliessen,co.re_auge_schliessen,"Neuwert: ",links_neuwert,rechts_neuwert)
                #print("linker ausgelesener Wert: ", links_readwert,"Konstant: ",co.arm_heben)
                #print("rechter ausgelesener Wert: ", rechts_readwert,"Konstant: ",co.arm_heben)

#                if links_readwert == co.li_auge_schliessen and rechts_readwert == co.re_auge_schliessen:
#                   sprache="aber meine Augen sind schon zu"
#                   sprachausgabe('"%s"' %sprache)
#                else:
                    #print("Inder Else: ",wenigtmp)
#                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        
                        #print("Hier beide ab: ",wenigtmp)
#                        links_neuwert = links_readwert - 25
#                        rechts_neuwert = rechts_readwert - 25
                        #print("Linkerneuwert nach addition. ",links_neuwert)
                        #print("Rechterneuwert nach addition. ",rechts_neuwert)
                        
#                        if links_neuwert >= co.li_auge_schliessen and rechts_neuwert >= co.re_auge_schliessen:

#                            links_neuwert = co.li_auge_schliessen
#                            rechts_neuwert = co.re_auge_schliessen
                            
#                            sprache="aber meine Augen sind schon zu"                              
#                            sprachausgabe('"%s"' %sprache)
 
                            #print("Scheiß_neuwert: ",neuwert)        
    
                    #print("Hier sollten sich die Arme bewegen: ", rechts_neuwert, links_neuwert)
#                    SI.move_servo(co.rechtes_lid,rechts_neuwert, speed_slow) 
#                    SI.move_servo(co.linkes_lid,links_neuwert, speed_slow)
 
#def auge_oeffnen(kttmp,seitetmp,speed_slow,wenigtmp):
            #print("Servo Nummern: ",co.linken_arm, co.rechten_arm)
    
    
# Zum debuggen Ausgabe der Werte  aktivieren         
           #print("Bin im heben modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)             

#            if seitetmp == "li":
                #print("Bin da")

#                readwert = SI.read_servopos(co.linkes_lid) 
                #print("links: ",readwert)     # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
#                neuwert = co.auge_oeffnen                          # Wichtig falls die wenigtempschleife nicht durchlaufen wird
#                print("ausgelesener Wert: ", readwert,"Konstant: ",co.li_auge_oeffnen,"Neuwert: ",neuwert)

#                if readwert == co.li_auge_oeffnen:
                    #print("Pups")
#                    sprache="aber mein linkes Auge ist schon auf"
#                    sprachausgabe('"%s"' %sprache)
#                else:
                    #print("Inder Else: ",wenigtmp)
#                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        #print("Hier ab: ",wenigtmp)
#                        neuwert = readwert - 25
                        #print("Neuwert nach addition. ",neuwert)
#                        if neuwert >= co.li_auge_oeffnen:
#                            neuwert = co.li_auge_oeffnen              # Den Wert sicherheitshalber auf den maximalen Wert setzen
                            #sprache="aber mein linkes Auge ist schon auf"    
                            #sprachausgabe('"%s"' %sprache) 
                            #print("Scheiß_neuwert: ",neuwert)        
                    #print("heb heb", neuwert)    
#                    SI.move_servo(co.linkes_lid,neuwert, speed_slow) 
                   
#            elif seitetmp == "re":
#                readwert = SI.read_servopos(co.rechtes_lid)
                #print("Read rechter arm: ",readwert,co.rechten_arm)         # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
#                neuwert = co.re_auge_oeffnen                              # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                #print("ausgelesener Wert: ", readwert)
#                print("ausgelesener Wert: ", readwert,"Konstant: ",co.re_auge_oeffnen,"Neuwert: ",neuwert)
                
#                if readwert == co.re_auge_oeffnen:
#                   sprache="aber mein rechtes Auge ist schon auf"
#                   sprachausgabe('"%s"' %sprache)               
#                else:
                     #print("Inder Else: ",wenigtmp)
#                    if wenigtmp == 'ab':
                        #print("Hier ab: ",wenigtmp)
#                        neuwert = readwert - 25
                        #print("Neuwert nach addition. ",neuwert)
#                        if neuwert >= co.re_auge_oeffnen:
#                            neuwert = co.re_auge_oeffnen 
                            #print("Scheiß_neuwert: ",neuwert)        
                    #print("heb heb", neuwert)    
#                    SI.move_servo(co.rechtes_lid,neuwert, speed_slow)    
                     
               
#            elif seitetmp == "be":
#                links_readwert = SI.read_servopos(co.linkes_lid)        # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
#                rechts_readwert = SI.read_servopos(co.rechtes_lid)      # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
#                links_neuwert = co.li_auge_oeffnen
#                rechts_neuwert = co.re_auge_oeffnen
#                print("ausgfrom datetime import datetime, timedeltagelesener Wert: ", links_readwert,rechts_readwert,"Konstant: ",co.li_auge_oeffnen,co.re_auge_oeffnen,"Neuwert: ",links_neuwert,rechts_neuwert)
                #print("linker ausgelesener Wert: ", links_readwert,"Konstant: ",co.arm_heben)
                #print("rechter ausgelesener Wert: ", rechts_readwert,"Konstant: ",co.arm_heben)

#                if links_readwert == co.li_auge_oeffnen and rechts_readwert == co.re_auge_oeffnen:
#                   sprache="aber meine Augen sind schon auf"
#                   sprachausgabe('"%s"' %sprache)
#                else:
                    #print("Inder Else: ",wenigtmp)
#                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        
                        #print("Hier beide ab: ",wenigtmp)
#                        links_neuwert = links_readwert - 25
#                        rechts_neuwert = rechts_readwert - 25
                        #print("Linkerneuwert nach addition. ",links_neuwert)
                        #print("Rechterneuwert nach addition. ",rechts_neuwert)
                        
#                        if links_neuwert >= co.li_auge_oeffnen and rechts_neuwert >= co.re_auge_oeffnen:

#                            links_neuwert = co.li_auge_oeffnen
#                            rechts_neuwert = co.re_auge_oeffnen
                            
#                            sprache="aber meine Augen sind schon auf"                              
#                            sprachausgabe('"%s"' %sprache)
 
                            #print("Scheiß_neuwert: ",neuwert)        
    
                    #print("Hier sollten sich die Arme bewegen: ", rechts_neuwert, links_neuwert)
#                    SI.move_servo(co.rechtes_lid,rechts_neuwert, speed_slow) 
#                    SI.move_servo(co.linkes_lid,links_neuwert, speed_slow)