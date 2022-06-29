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

from datetime import datetime, timedelta
#Temp
import importlib
importlib.reload(sys)
#from gpiozero import LED
#from pixel_ring import pixel_ring

 
import requests

import globs
#import threading

def uhrz(dat,tageswert):

    datum=""
    wotag=""
    
    print("Hier ist die Uhrzeit:  uhrzeit_incl.py uhrz()")
    #print("Intent wert1: ",wert1,"Value: ",wert1_value)
    print("Intent: ",dat,"Value: ",tageswert)
    
    #print(wert1,wert1_value,wert2,wert2_value)
    now = datetime.now()
    wtagname = now.strftime("%w")
    
    if tageswert == "heute":
        wtag=MY.numwandel(now.strftime("%-d"))
        monat=MY.numwandel(now.strftime("%-m"))
        monatname=calendar.month_name[int(now.strftime("%-m"))]
        #print("Kuckuck Monatsname: ",monatname,"Datum: ",dat)
        datum = wtag+" "+monat+" "+now.strftime("%Y")
        ist=" ist "

    elif tageswert == "übermorgen":
        morgen = datetime.now() + timedelta(2)
        wtagname = morgen.strftime("%w")
        wtag=MY.numwandel(morgen.strftime("%-d"))
        monat=MY.numwandel(morgen.strftime("%-m"))
        monatname=calendar.month_name[int(morgen.strftime("%-m"))]
        #print("Monatsname: ",monatname)
        datum = wtag+" "+monat+" "+morgen.strftime("%Y")
        ist=" ist "
        
    elif tageswert == "morgen":
        print("Pups------")
        morgen = datetime.now() + timedelta(1)
        wtagname = morgen.strftime("%w")
        wtag=MY.numwandel(morgen.strftime("%-d"))
        monat=MY.numwandel(morgen.strftime("%-m"))
        monatname=calendar.month_name[int(morgen.strftime("%-m"))]
        #print("Monatsname: ",monatname)
        datum = wtag+" "+monat+" "+morgen.strftime("%Y")
        ist=" ist "
        print("Morgen: ",datum)
        
    elif tageswert == "gestern":
        morgen = datetime.now() + timedelta(-1)
        wtagname = morgen.strftime("%w")
        wtag=MY.numwandel(morgen.strftime("%-d"))
        monat=MY.numwandel(morgen.strftime("%-m"))
        monatname=calendar.month_name[int(morgen.strftime("%-m"))]
        #print("Monatsname: ",monatname)
        datum = wtag+" "+monat+" "+morgen.strftime("%Y")
        ist=" war "
        
    elif tageswert == "vorgestern":
        morgen = datetime.now() + timedelta(-2)
        wtagname = morgen.strftime("%w")
        wtag=MY.numwandel(morgen.strftime("%-d"))
        monat=MY.numwandel(morgen.strftime("%-m"))
        monatname=calendar.month_name[int(morgen.strftime("%-m"))]
        #print("Monatsname:  ",monatname)
        datum = wtag+" "+monat+" "+morgen.strftime("%Y")
        ist=" war "        
        
    if dat == 'Tag' or dat == "datum":

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
        
    elif dat == "Monat":
        sprache=globs.speaker+" Wir haben "+monatname 
         
    else:
        sprache = globs.speaker+" Es ist "+now.strftime("%-H")+" Uhr "+now.strftime("%M")

    #sprachausgabe('"%s"' %sprache)
    MY.sprachausgabe('"%s"' %sprache)


