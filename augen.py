  #!/usr/bin/env python3
# encoding: utf-8
from __future__ import print_function
from __future__ import division
import paho.mqtt.client as mqtt 
import json
from random import randint
import os
import glob
import time
import constant as co
import Servo_Include as SI
import sys
import calendar
import datetime
from datetime import timedelta
#Temp
import importlib
importlib.reload(sys)

#sys.setdefaultencoding('utf8')
import mylib as MY
# import required modules 
import requests


    
def auge_schliessen(kttmp,subkttmp,seitetmp,speed_slow,wenigtmp):
    
# Zum debuggen Ausgabe der Werte  aktivieren         
           #print("Bin im heben modul: ",kttmp,seitetmp,speedtmp,wenigtmp,speed_slow)             

            if seitetmp == "li":
                readwert = SI.read_servopos(co.linkes_lid) 
                neuwert = co.li_auge_schliessen                          # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                #print("ausgelesener Wert: ", readwert,"Konstant: ",co.li_auge_schliessen,"Neuwert: ",neuwert)

                if readwert == co.li_auge_schliessen:
                    sprache="aber mein linkes Auge ist schon zu"
                    MY.sprachausgabe('"%s"' %sprache)
                else:
                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        neuwert = readwert - 25
                        if neuwert >= co.li_auge_schliessen:
                            neuwert = co.li_auge_schliessen              # Den Wert sicherheitshalber auf den maximalen Wert setzen
                            sprache="aber mein linkes Auge ist schon zu"    
                            MY.sprachausgabe('"%s"' %sprache) 
                    SI.move_servo(co.linkes_lid,neuwert, speed_slow) 
                   
            elif seitetmp == "re":
                readwert = SI.read_servopos(co.rechtes_lid)
                neuwert = co.re_auge_schliessen                              # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                #print("ausgelesener Wert: ", readwert,"Konstant: ",co.re_auge_schliessen,"Neuwert: ",neuwert)
                
                if readwert == co.re_auge_schliessen:
                   sprache="aber mein rechtes Auge ist schon zu"
                   MY.sprachausgabe('"%s"' %sprache)               
                else:
                    if wenigtmp == 'ab':
                        neuwert = readwert - 25
                        if neuwert >= co.re_auge_schliessen:
                            neuwert = co.re_auge_schliessen 
                    SI.move_servo(co.rechtes_lid,neuwert, speed_slow)    
                     
               
            elif seitetmp == "be":
                #try:
                links_readwert = SI.read_servopos(co.linkes_lid)        # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                rechts_readwert = SI.read_servopos(co.rechtes_lid)      # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                #except Exception as e:
                #    print(e)
                    
                links_neuwert = co.li_auge_schliessen
                rechts_neuwert = co.li_auge_schliessen
                #print("ausgfrom datetime import datetime, timedeltaelesener Wert: ", rechts_readwert," ", links_readwert, "Konstant: ",co.li_auge_schliessen,co.re_auge_schliessen,"Neuwert: ",links_neuwert,rechts_neuwert)

                if links_readwert == co.li_auge_schliessen and rechts_readwert == co.re_auge_schliessen:
                   sprache="aber meine Augen sind schon zu"
                   MY.sprachausgabe('"%s"' %sprache)
                else:
                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        links_neuwert = links_readwert - 25
                        rechts_neuwert = rechts_readwert - 25
                        
                        if links_neuwert >= co.li_auge_schliessen and rechts_neuwert >= co.re_auge_schliessen:

                            links_neuwert = co.li_auge_schliessen
                            rechts_neuwert = co.re_auge_schliessen
                            
                            sprache="aber meine Augen sind schon zu"                              
                            MY.sprachausgabe('"%s"' %sprache)
 
                    SI.move_servo(co.rechtes_lid,rechts_neuwert, speed_slow) 
                    SI.move_servo(co.linkes_lid,links_neuwert, speed_slow)
 
def auge_oeffnen(kttmp,subkttmp,seitetmp,speed_slow,wenigtmp):
# Zum debuggen Ausgabe der Werte  aktivieren         
            if seitetmp == "li":
                readwert = SI.read_servopos(co.linkes_lid) 
                neuwert = co.auge_oeffnen                          # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                print("ausgelesener Wert: ", readwert,"Konstant: ",co.li_auge_oeffnen,"Neuwert: ",neuwert)

                if readwert == co.li_auge_oeffnen:
                    sprache="aber mein linkes Auge ist schon auf"
                    MY.sprachausgabe('"%s"' %sprache)
                else:
                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        neuwert = readwert - 25
                        if neuwert >= co.li_auge_oeffnen:
                            neuwert = co.li_auge_oeffnen              # Den Wert sicherheitshalber auf den maximalen Wert setzen
                    SI.move_servo(co.linkes_lid,neuwert, speed_slow) 
                   
            elif seitetmp == "re":
                readwert = SI.read_servopos(co.rechtes_lid)
                neuwert = co.re_auge_oeffnen                              # Wichtig falls die wenigtempschleife nicht durchlaufen wird
                print("ausgelesener Wert: ", readwert,"Konstant: ",co.re_auge_oeffnen,"Neuwert: ",neuwert)
                
                if readwert == co.re_auge_oeffnen:
                   sprache="aber mein rechtes Auge ist schon auf"
                   MY.sprachausgabe('"%s"' %sprache)               
                else:
                    if wenigtmp == 'ab':
                        neuwert = readwert - 25
                        if neuwert >= co.re_auge_oeffnen:
                            neuwert = co.re_auge_oeffnen 
                    SI.move_servo(co.rechtes_lid,neuwert, speed_slow)    
                     

            elif seitetmp == "be":
                links_readwert = SI.read_servopos(co.linkes_lid)        # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                rechts_readwert = SI.read_servopos(co.rechtes_lid)      # Die letzte Position des Servos auslesen , ist bei einer größeren Anzahl von Körperteilen für jedes notwendig
                links_neuwert = co.li_auge_oeffnen
                rechts_neuwert = co.re_auge_oeffnen
                print("ausgfrom datetime import datetime, timedeltagelesener Wert: ", links_readwert,rechts_readwert,"Konstant: ",co.li_auge_oeffnen,co.re_auge_oeffnen,"Neuwert: ",links_neuwert,rechts_neuwert)

                if links_readwert == co.li_auge_oeffnen and rechts_readwert == co.re_auge_oeffnen:
                   sprache="aber meine Augen sind schon auf"
                   MY.sprachausgabe('"%s"' %sprache)
                else:
                    if wenigtmp == 'ab':                        # wenn nur eine kleine Bewegung gewünscht wird
                        
                        links_neuwert = links_readwert - 25
                        rechts_neuwert = rechts_readwert - 25
                        
                        if links_neuwert >= co.li_auge_oeffnen and rechts_neuwert >= co.re_auge_oeffnen:

                            links_neuwert = co.li_auge_oeffnen
                            rechts_neuwert = co.re_auge_oeffnen
                            
                            sprache="aber meine Augen sind schon auf"                              
                            MY.sprachausgabe('"%s"' %sprache)
 
                    SI.move_servo(co.rechtes_lid,rechts_neuwert, speed_slow) 
                    print("Bubu")
                    SI.move_servo(co.linkes_lid,links_neuwert, speed_slow)
