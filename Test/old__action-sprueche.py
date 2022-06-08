#!/usr/bin/env python3
# encoding: utf-8
from __future__ import print_function
import paho.mqtt.client as mqtt 
import json
from random import randint
import os
import glob
#import platform
import datetime
#print(platform.python_version())
global na
na=[]
global ess
ess=[]
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
a_na=1
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

def on_connect(client, userdata, flags, rc): 
    #print('Connected') 
    mqtt.subscribe('hermes/intent/dsgra:Sprueche')

def on_message(client, userdata, msg):
    json_data = json.loads(msg.payload.decode('utf-8'))
    slots = parse_slots(json_data)
    #name = json_data["intent"]["intentName"]
    sprueche_slots = list(slots.keys())[0]
    sprueche(sprueche_slots)

def parse_slots(wert):
    '''
    We extract the slots as a dict
    '''
    #data = json.loads(msg) # .payload
    data = wert 
    return dict((slot['slotName'], slot['rawValue']) for slot in data['slots'])
        
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

#def get_sprueche():
#    file_list=os.listdir("sprueche")
#    print(file_list)


def write_speaker(speaker):
    print(speaker)
    file=open("/tmp/speaker.txt","w")
    file.write(str(speaker))
    file.close()

def read_speaker():
    try:   
        file=open("/tmp/speaker.txt","r")
        speaker = file.readline()
        file.close()
    except FileNotFoundError:
        speaker = ""
    return speaker      

def sprueche(nslots):
    # Der Sprecher wird aus der Dastei /tmp/speaker.txt ausgelesen
    speaker = read_speaker()
    if speaker == "Thomas":
        rest_speaker = "bist Du"
    else:
        rest_speaker = "Thomas"

  #print("Der Sprecher war: " + speaker)
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

    kt = str(nslots)
    #print(kt)
    if kt == 'KT_gNacht':
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

    elif kt == 'KT_werbinich':       
        wer = wert_entfernen(wer[0], a_wer)
        spruch = 'wer' + str(wer[2])
    elif kt == 'KT_Tschuess':       
        ts = wert_entfernen(ts[0], a_ts)
        spruch = 'ts' + str(ts[2])
    elif kt == 'KT_besserwiss':       
        bw = wert_entfernen(bw[0], a_bw)
        spruch = 'bw' + str(bw[2])
    elif kt == 'KT_name':       
        nw = wert_entfernen(na[0], a_na)
        spruch = 'na' + str(na[2])
    elif kt == 'KT_essen':       
        ess = wert_entfernen(ess[0], a_ess)
        spruch = 'ess' + str(ess[2])
    elif kt == 'KT_einkaufen':       
        ek = wert_entfernen(ek[0], a_ek)
        spruch = 'ek' + str(ek[2])
    elif kt == 'KT_Vater':       
        va = wert_entfernen(va[0], a_va)
        spruch = 'va' + str(va[2])
    elif kt == 'KT_gemacht':
        ge = wert_entfernen(ge[0], a_ge)
        spruch = 'ge' + str(ge[2])
    elif kt == 'KT_befinden':
        be = wert_entfernen(be[0], a_be)
        spruch = 'be' + str(be[2])
    elif kt == 'KT_putzen':
        pu = wert_entfernen(pu[0], a_pu)
        spruch = 'pu' + str(pu[2])
    elif kt == 'KT_aufraeumen':
        auf = wert_entfernen(auf[0], a_auf)
        spruch = 'auf' + str(auf[2])
    #print("jetzt da")
    #print(spruch)

    with open ("sprueche/" + spruch + ".txt", "r") as mline:
    #with open ("/usr/local/sprueche/" + spruch + ".txt", "r") as mline:
       
       sline='"' + str(mline.read().replace('\n', '')) + '"'
       eline = sline.replace('*', rest_speaker)
       nline=eline.replace('#', speaker)
    #   print(nline)
       sprache = "{\"text\":" + nline + ",\"lang\":\"de\",\"siteId\":\"default\",\"sessionID\":2711}"
       mqtt.publish("hermes/tts/say", sprache)

    print(sprache)

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

mqtt = mqtt.Client() 
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect('localhost', 1883) 
mqtt.loop_forever()


