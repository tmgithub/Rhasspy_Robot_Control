  #!/usr/bin/env python3
# encoding: utf-8
from __future__ import print_function
from __future__ import division

from random import randint
import os
import subprocess
import glob
import time
import constant as co
import mylib as MY
import sys
import calendar
import datetime
from datetime import datetime, timedelta
#Temp
import importlib
importlib.reload(sys)
from gpiozero import LED
from pixel_ring import pixel_ring

 
import requests

import globs
import threading

def uhrzeit(wert1,wert1_value,wert2,wert2_value):
    tageswert=wert2_value
    datum=""
    wotag=""
    
    print("Hier ist die Uhrzeit:  uhrzeit_incl.py uhrzeit()")
    print("Intent wert1: ",wert1,"Value: ",wert1_value)
    print("Intent wert2: ",wert2,"Value: ",wert2_value)
    
    #print(wert1,wert1_value,wert2,wert2_value)
    now = datetime.now()
    wtagname = now.strftime("%w")
    
    if wert2_value == "heute":
        wtag=MY.numwandel(now.strftime("%-d"))
        monat=MY.numwandel(now.strftime("%-m"))
        monatname=calendar.month_name[int(now.strftime("%-m"))]
        #print("Monatsname: ",monatname)
        datum = wtag+" "+monat+" "+now.strftime("%Y")
        ist=" ist "

    elif wert2_value == "übermorgen":
        morgen = datetime.now() + timedelta(2)
        wtagname = morgen.strftime("%w")
        wtag=MY.numwandel(morgen.strftime("%-d"))
        monat=MY.numwandel(morgen.strftime("%-m"))
        monatname=calendar.month_name[int(morgen.strftime("%-m"))]
        #print("Monatsname: ",monatname)
        datum = wtag+" "+monat+" "+morgen.strftime("%Y")
        ist=" ist "
        
    elif wert2_value == "morgen":
        morgen = datetime.now() + timedelta(1)
        wtagname = morgen.strftime("%w")
        wtag=MY.numwandel(morgen.strftime("%-d"))
        monat=MY.numwandel(morgen.strftime("%-m"))
        monatname=calendar.month_name[int(morgen.strftime("%-m"))]
        #print("Monatsname: ",monatname)
        datum = wtag+" "+monat+" "+morgen.strftime("%Y")
        ist=" ist "
        
    elif wert2_value == "gestern":
        morgen = datetime.now() + timedelta(-1)
        wtagname = morgen.strftime("%w")
        wtag=MY.numwandel(morgen.strftime("%-d"))
        monat=MY.numwandel(morgen.strftime("%-m"))
        monatname=calendar.month_name[int(morgen.strftime("%-m"))]
        #print("Monatsname: ",monatname)
        datum = wtag+" "+monat+" "+morgen.strftime("%Y")
        ist=" war "
        
    elif wert2_value == "vorgestern":
        morgen = datetime.now() + timedelta(-2)
        wtagname = morgen.strftime("%w")
        wtag=MY.numwandel(morgen.strftime("%-d"))
        monat=MY.numwandel(morgen.strftime("%-m"))
        monatname=calendar.month_name[int(morgen.strftime("%-m"))]
        #print("Monatsname:  ",monatname)
        datum = wtag+" "+monat+" "+morgen.strftime("%Y")
        ist=" war "        
        
    if wert1_value == 'Tag' or wert1_value == "datum":

        if wtagname == "1":
            wotag = "Montag"
        elif wtagname == "2":
            wotag = "Dienstag"
        elif wtagname == "3":
            wotag = "Mittwoch"
        elif wtagname == "4":
            wotag = "Donnerstag"
        elif wtagname == "5":
            wotag = "Freitag"
        elif wtagname == "6":
            wotag = "Samstag"
        elif wtagname == "7":
            wotag = "Sonntag"
        sprache = globs.speaker+" "+tageswert+ist+wotag+" der "+datum
        
    elif wert1_value == "Monat":
        sprache=globs.speaker+" Wir haben "+monatname 
         
    else:
        sprache = globs.speaker+" Es ist "+now.strftime("%-H")+" Uhr "+now.strftime("%M")

    MY.sprachausgabe('"%s"' %sprache)