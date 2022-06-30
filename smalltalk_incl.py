#!/usr/bin/env python3
# encoding: utf-8

## benötigt das Verzeichnis sprueche mit entsprechenden Textdateien
from __future__ import print_function
import paho.mqtt.client as mqtt 
import json
from random import randint
import os
import glob
#import platform
import datetime
import mylib as MY

import globs
#print(platform.python_version())

global na
na=[]
global ess
ess=[]
global tri
tri=[]
global gn
gn=[]
global ts
ts=[]
global wer
wer=[]
global bw
bw=[]
global ek
ek=[]
global va
va=[]
global ge
ge=[]
global be
be=[]
global pu
pu=[]
global auf
auf=[]


global a_ess
a_ess = 5
global a_tri
a_tri = 2
global a_bw
a_bw=2
global a_wer
a_wer=3
global a_ts
a_ts =  7
global a_gn
a_gn = 11
global a_ek
a_ek=2
global a_na
a_na=2
global a_va
a_va=1
global a_ge
a_ge=2
global a_be
a_be=2
global a_pu
a_pu=5
global a_auf
a_auf=3


global apos
global kt

def list_all(filename):
    count = 0
    searchfile='sprueche/' + filename + '*'

    for name in glob.glob(searchfile):
        count = count + 1 
    return count    

        
def init_myliste(aname, aanzahl):
    # leeres Array anlegen
    aname = [] 
    # Array befüllen mit Werten 1 -> aanzahl
    for x in range(1,aanzahl + 1):
        aname.append(x)
    #print("Init: " + str(aname[1]) + " " +  str(aanzahl)) 
    return(aname, aanzahl)    

def wert_entfernen(aname, a_len):
    apos = 1 
    # Anzahl der Arrayeinträge ermitteln
    anzahl = len(aname) - 1
    if anzahl > 0:
        #print("Länge des Arrays: " + str(anzahl + 1))    
    # Zufallszahl abhängig von der länge des Arrays generieren
        apos = randint(1,anzahl) - 1
    # Wert des Arrayinhalts auslesen
        aval = aname[apos]
        #print("Inhalt Arraywert: " + str(aval))
    
    # Eintrag aus dem Array löschen
        del aname[apos]
    
    # Wnn der letzte Wert erreicht worden ist das Array neu befüllen
    else:
        aname = init_myliste(aname, a_len)[0]
        aval = a_len
    return(aname, apos, aval)

def sprueche(sttmp,vwtmp,subvwtmp):
    #print("Jetzt in Sprueche: ")
    # Der Sprecher wird aus der in globs definierten Variable speaker geholt aber nur wenn niocht nobody opder default
    
    if globs.speaker == "default" or globs.speaker == "nobody":
        speaker = ""
    else:
        speaker = globs.speaker
        
    #print("Hallo hier: ")
    print("Hier geht der Smalltalk weiter: smalltalk_incl.py def sprueche()")
    print(" ")
    print("VWTMP: ",vwtmp,"STTMP: ",sttmp,"subvwtmp: ",subvwtmp)

    if globs.speaker == "Thomas":
        rest_speaker = "bist Du"
    else:
        rest_speaker = "Thomas"

    print("Der Sprecher war: " + globs.speaker)
    global gn
    global wer 
    global ts
    global bw 
    global ess
    global ek
    global na
    global va
    global ge
    global be
    global pu
    global auf
    global tri

    #print(kt)
    trifftzu = 0
    
    if sttmp == 'GNACHT':
        trifftzu = 1
        hours = datetime.datetime.now().hour
        if hours >= 9 and hours <= 12:
           spruch = "gn0"
        elif hours > 12 and hours <= 14:
            spruch = "gn01"
        elif hours > 14 and hours <= 18:
           spruch  = "gn00"
        else:
           gn = wert_entfernen(gn[0], a_gn)
           spruch = 'gn' + str(gn[2])

    #elif wert1 == 'KT_werbinich':       
    #    wer = wert_entfernen(wer[0], a_wer)
    #    spruch = 'wer' + str(wer[2])
    elif sttmp == 'TSCHUESS':
        trifftzu = 1       
        ts = wert_entfernen(ts[0], a_ts)
        spruch = 'ts' + str(ts[2])
        
    elif sttmp == 'BESSERWISS': 
        trifftzu = 1       
        bw = wert_entfernen(bw[0], a_bw)
        spruch = 'bw' + str(bw[2])
    
    elif sttmp == 'NAME': 
        trifftzu = 1
        print("Das ist es: ")      
        na = wert_entfernen(na[0], a_na)
        print("na ist weg ")
        spruch = 'na' + str(na[2])
        print(spruch)
        
    elif sttmp == 'ESSEN':       
        trifftzu = 1
        ess = wert_entfernen(ess[0], a_ess)
        spruch = 'ess' + str(ess[2])
        
    elif sttmp == 'WERBIST':       
        trifftzu = 1
        wer = wert_entfernen(wer[0], a_wer)
        spruch = 'wer' + str(wer[2])
        print("Spruch: ",spruch)
                
    elif sttmp == 'TRINKEN':       
        trifftzu = 1
        tri = wert_entfernen(tri[0], a_tri)
        spruch = 'tri' + str(tri[2])
        
    elif sttmp == 'PUTZEN':       
        trifftzu = 1
        pu = wert_entfernen(pu[0], a_pu)
        spruch = 'pu' + str(pu[2])
        
    elif sttmp == 'KAUF':       
        trifftzu = 1
        ek = wert_entfernen(ek[0], a_ek)
        spruch = 'ek' + str(ek[2])
        
    elif sttmp == 'NOKAUF':       
        trifftzu = 0
        tmpnline = "Dann brauchst Du mir ja auch nichts mitbringen."  
        nline = tmpnline  

        
    elif sttmp == 'VERWNAME':
         print("Hier oder was")
         trifftzu = 0
             
         w2temp = wert1_value.split("_")
         print("Wert2: ",w2temp)
         nline = "Hallo "+ w2temp[0]+" ."
         
    elif sttmp == "HAIRCUT":
        triftzu = 0
        tmpnline = "Das lass mal lieber vom Profi, Frau Paegel, machen."  
        nline = tmpnline  

         
    elif subvwtmp == "VERWANDT":
        trifftzu = 0   
        delimiter ="_"
        slots = vwtmp.split(delimiter)
        
        if slots[0] == vwtmp:
            print("Name: ",vwtmp)
            nline = "Ich kenne "+vwtmp
        else:
            verwname = slots[0]
            verw = slots[1]
            print("Verw: ",verw)
            print("Verwname: ",verwname) 
            if verw =="TANTE" or verw=="TOCHTER" or verw=="MUTTER":
                plural = "e "
            else: 
                plural =""   
            tmpnline = "Mein"+ plural +" "+ verw +" ist " + verwname

            nline = str(tmpnline)
            print("nline: ",nline)
        

#slots = input_string.split(delimiter)
#if slots[0] == input_string:
#  print('no %s found' % delimiter)
#else:
#  print('%s found right after \"%s\"' % (delimiter, slots[0]))      

    elif subvwtmp == 'VERWNAME':
        print("Hier geht der Smalltalk weiter: smalltalk_incl.py def sprueche() if wert2 = VERWNAME")
        
        trifftzu = 0

        w2temp = wert1.split("_")
        print("Wert1: ",w2temp)
        
        if wert3 == "INTRO":
            print("Intro: ")
            nline ="Hallo "+w2temp[0]+". Du bist also "+w2temp[2]+" "+w2temp[1]+ " !"

        else:
            if wert1_value == 'thomas':
               nline = "Du heißt ja so wie mein Erbauer oder bist du es sogar selbst?"
            
            elif wert1_value == 'heike':
               nline ="Bist Du meine Mutter die Frau von meinen Erbauer Thomas ?"
            else:
               nline=w2temp[0]+" ist "+w2temp[2]+ " "+w2temp[1]
         
        
    elif sttmp == "BELEIDIGUNG":
        trifftzu = 0
        nline= "Bitte keine Beleidigungen."                              

    elif sttmp == "TAETIGKEIT":
        trifftzu = 0
        nline = speaker+" Leider kann ich nicht " +wert1_value+" ."

    if trifftzu > 0:    
        print("jetzt da")
    #print(spruch)
        with open ("sprueche/" + spruch + ".txt", "r") as mline:
        
    #with open ("/usr/local/sprueche/" + spruch + ".txt", "r") as mline:
       
            sline='"' + str(mline.read().replace('\n', '')) + '"'
            eline = sline.replace('*', rest_speaker)
            tline=eline.replace('#', speaker)
            nline=tline.replace('"',"")
            
            print("Spruch: ",nline)
    #MY.sprachausgabe(nline)
    MY.sprachausgabe('"%s"' %nline)
    #MY.sprachausgabe(nline)
        



       

a_gn = list_all('gn')
gn = init_myliste(gn,a_gn)

a_ts = list_all('ts')
ts = init_myliste(ts,a_ts)

a_wer = list_all('wer')
wer = init_myliste(wer,a_wer)

a_bw = list_all('bw')
bw = init_myliste(bw,a_bw)

a_na = list_all('na')
na = init_myliste(na,a_na)

a_ek = list_all('ek')
ek = init_myliste(ek,a_ek)

a_ess = list_all('ess')
ess = init_myliste(ess,a_ess)

a_tri = list_all('tri')
tri = init_myliste(tri,a_tri)

a_va = list_all('va')
va = init_myliste(va,a_va)

a_ge = list_all('ge')
ge = init_myliste(ge,a_ge)

a_be = list_all('be')
be = init_myliste(be,a_be)

a_pu = list_all('pu')
pu = init_myliste(pu,a_pu)

a_auf = list_all('auf')
auf = init_myliste(auf,a_auf)


