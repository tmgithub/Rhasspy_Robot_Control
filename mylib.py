  #!/usr/bin/env python3
# encoding: utf-8
from __future__ import print_function
from __future__ import division
import paho.mqtt.client as mqtt 
import paho.mqtt.publish as mqttpublish
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



def parse_slots(wert):
    '''
    We extract the slots as a dict
    '''
    #data = json.loads(msg) # .payload
    data = wert 
    return dict((slot['slotName'], slot['value']) for slot in data['slots'])
        
#def read_speaker():
#    try:   
#        file=open("/tmp/speaker.txt","r")
#        speaker = file.readline()
#        file.close()
#    except FileNotFoundError:
#        speaker = ""
#    return speaker
    
def placechange(nameslot,slots):
   # global kt
    #global seite
    #global speed
    #global wenig
    #global real_speed
    #global real_seite
    #global real_wenig
    globs.kt=""
    seite=""
    speed=""
    wenig=""
    real_speed=""
    real_seite=""
    real_wenig=""

    for i in range(len(nameslot)):
        if "KT" in nameslot[i]:
            kt = (slots[nameslot[i]])['value']
        elif "ReLi" in nameslot[i]:    
            seite = (slots[nameslot[i]])['value'][:2]
            real_seite = (slots[nameslot[i]])['value']
        elif "SLOW" in nameslot[i]:
            speed = (slots[nameslot[i]])['value']
            real_speed="langsam"
        elif "ABIT" in nameslot[i]:
            wenig = (slots[nameslot[i]])['value'][:2]
            real_wenig="ein wenig"
    return kt,seite,speed,wenig,real_seite,real_speed,real_wenig

def sprachausgabe(satz):
    pixel_ring.speak()
    print("mylib.py sprachausgabe(): ",satz)
    tospeak_payload=json.dumps({'text': satz,'siteId': 'default', 'modelId': 'default'})
    print("Sprecher: ",globs.speaker)

    publish("hermes/tts/say",tospeak_payload)
    #print("Satz: ",syssentence) 
    #subprocess.run(syssentence,shell=True,stdout=subprocess.DEVNULL)
    #subprocess.run(sysplay,shell=True,stdout=subprocess.DEVNULL)
    pixel_ring.listen()
    #os.system(syssentence)
    #os.system(sysplay)

def wohlbefinden():
    try:   
        file_temperatur="/sys/class/thermal/thermal_zone0/temp"
        #print("Datei: ",file_temperatur)
        #print("Datei : ",file_servo)
        file=open(file_temperatur,"r")
        temperatur = str(int(int(file.readline())/1000))
        file.close()
        
        #print("Temperatur ist: ",temperatur)
    except Exception as e:     # wenn die Datei nicht vorhanden ist oder nicht gelesen werden kann den Servowert auf neutral setzen
         print(e)
    return (temperatur)#, Hauptmem, Freimem)


#wert1="'ich bin der Thomas'"
#sprachausgabe(wert1)


                     
                    
                    
                    
def bein_heben(kttmp,seitetmp,speed_slow,wenigtmp):
    pass

def wind_deg2txt(deg):
    #                 0   1    2   3    4   5    6   7    8
    wind_dir_name = ['Norden','NordOsten','Osten','SüdOsten','Süden','SüdWesten','Westen','NordWesten','Norden']
 
    wind_sections = 360 / 8
    offset = wind_sections / 2 
    # range(start, stop[, step])
    y = int( (deg + offset) / wind_sections )
    #print(y)

    #print(deg, y, offset, wind_sections)
    wind_dir_txt = wind_dir_name[y]
    #print(" -> " + wind_dir_txt)
 
    return(wind_dir_txt)


def wetter(wettmp,orttmp,subwettmp):
    print("mylib.py wetter()")
# Python program to find current 
# weather details of any city 
# using openweathermap api  

# Enter your API key here 
    api_key = "0973b20b977793d834a490d9cc698d8e"

# base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    print("Wetter= ",wettmp,"Ort= ",orttmp)
    
    if orttmp != "":
        city_name = orttmp
    else:
        city_name ="Berlin"
    
    
    
# Give city name 
#
    #print("Stadt: ",city_name)

# complete_url variable to store 
# complete url address 
    complete_url = base_url + "appid=" + api_key + "&lang=de&units=metric&q=" + city_name 
    #print(complete_url)

# get method of requests module 
# return response object 
    response = requests.get(complete_url) 

# json method of response object 
# convert json format data into 
# python format data 
    x = response.json()

# Now x contains list of nested dictionaries 
# Check the value of "cod" key is equal to 
# "404", means city is found otherwise, 
# city is not found 
    if x["cod"] != "404": 

    # store the value of "main" 
    # key in variable y 
        y = x["main"] 
        wind = x["wind"]
        diverses = x["sys"]

    # store the value corresponding 
    # to the "temp" key of y 
        current_temperature = y["temp"] 

    # store the value corresponding 
    # to the "pressure" key of y 
        current_pressure = y["pressure"] 

    # store the value corresponding 
    # to the "humidity" key of y 
        current_humidiy = y["humidity"] 
        
        current_sunrise = diverses["sunrise"]+120
        current_sunset = diverses["sunset"]+120
        current_windspeed = wind["speed"]
        SoA= datetime.datetime.fromtimestamp(int(current_sunrise)).strftime('%-H:%-M')
        SoAufgang = SoA.replace(":"," Uhr ")
        SoU = datetime.datetime.fromtimestamp(int(current_sunset)).strftime('%-H:%-M')
        SoUntergang = SoU.replace(":"," Uhr ") 
        #SoAufgang = str(datetime.timedelta(seconds=current_sunrise))
        #print(SoAufgang)
        #print(SoUntergang)
        current_windrichtung = wind["deg"]
        #print(wind_deg2txt(current_windrichtung))
        #print(current_temperature,current_sunrise,current_sunset,current_windspeed,current_windrichtung)
    # store the value of "weather" 
    # key in variable z 
        z = x["weather"] 

    # store the value corresponding 
    # to the "description" key at 
    # the 0th index of z 
        heiss = ""
        if current_temperature >= 30:
            heiss = "es ist "+subwettmp
        elif current_temperature <=20:
            heiss = "es ist nicht "+subwettmp
            
        weather_description = z[0]["description"]  
        ct = str(current_temperature)
        ctemp = ct.replace("."," komma ")
        ldruck= str(current_pressure)
        lfeucht= str(current_humidiy)
        wist= str(current_windspeed)
        windstaerke = wist.replace(".", " komma ")
        windrichtung = wind_deg2txt(current_windrichtung)
        #print(weather_description)
        #sonnenaufgang =
        if wettmp == "ONLYTEMP":
            if subwettmp == "temperatur":
                heiss = ""
            sprache1 = "Die Temperatur in "+city_name+" beträgt "+ctemp+ " Grad Celsius . "+heiss
            sprache2 =""
            sprache3=""
            sprache4=""
        else:   
            sprache1 = "Die Temperatur in "+city_name+" beträgt "+ctemp+ " Grad Celsius, bei einem Luftdruck vom "+ldruck+" hektopascal und einer relativen Luftfeuchte von "+lfeucht+" Prozent . "
            sprache2 = weather_description+" mit einem Wind aus "+windrichtung+" mit einer Geschwindigkeit von "+windstaerke+" meter pro sekunde. "
            sprache3 = "Der Sonnenaufgang ist um "+SoAufgang
            sprache4 = "der Sonnenuntergang ist um "+SoUntergang

        if wettmp == "SOA":
            sprache = "In "+city_name+" ist der Sonnenaufgang um "+SoAufgang
        elif wettmp =="SOU":
            sprache = "In "+city_name+" ist der Sonnenuntergang um "+SoUntergang
        elif subwettmp == "temperatur":
            sprache = "Die Temperatur in "+city_name+" beträgt "+ctemp+ " Grad Celsius"
        else:
            sprache = sprache1+sprache2+sprache3+sprache4
        
        sprachausgabe('"%s"' %sprache)
    # print following values 
        #print(" Temperature (in Celsius) = " +
        #           str(int(current_temperature - 273.15)) +
        #            "\n atmospheric pressure (in hPa unit) = " +
        #            str(current_pressure) +
        #            "\n humidity (in percentage) = " +
        #            str(current_humidiy) +
        #            "\n description = " +
        #           str(weather_description)) 
#
    else: 
        print(" Stadt nicht gefunden ") 

def numwandel(wert):
    back="leer"
    #res = isinstance(wert, str)
    #print("Das ist der Wert: ",wert,res)
    if wert == "1":
        back = "erste"
    elif wert == "2":
        back = "zweite"
    elif wert == "3":
        back = "dritte"    
    elif wert == "4":
        back = "vierte"
    elif wert == "5":
        back = "fünfte" 
    elif wert == "6":
        back = "sechste"
    elif wert == "7":
        back = "siebente"
    elif wert == "8":
        back = "achte"
    elif wert == "9":
        back = "neunte"
    elif wert == "10":
        back = "zehnte"
    elif wert == "11":
        back = "elfte"
    elif wert == "12":
        back = "zwölfte"
    elif wert == "13":
        back = "dreizehnte"
    elif wert == "14":
        back = "vierzehnte"
    elif wert == "15":
        back = "fünfzehnte"
    elif wert == "16":
        back = "sechszehnte"
    elif wert == "17":
        back = "siebzehnte"
    elif wert == "18":
        back = "achtzehnte"
    elif wert == "19":
        back = "neunzehnte"
    elif wert == "20":
        back = "zwanzigste"
    elif wert == "21":
        back = "einundzwanzigste"
    elif wert == "22":
        back = "zweiundzwanzigste"
    elif wert == "23":
        back = "dreiundzwanzigste"
    elif wert == "24":
        back = "vierundzwanzigste"
    elif wert == "25":
        back = "fünfundzwanzigste"
    elif wert == "26":
        back = "sechsundzwanzigste"
    elif wert == "27":
        back = "siebenundzwanzigste"
    elif wert == "28":
        back = "achtundzwanzigste"
    elif wert == "29":
        back = "neunundzwanzigste"
    elif wert == "30":
        back = "dreizigste"
    elif wert == "31":
        back = "einunddreizigste"
    return back    


def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            TempHauptmem=str(int(line.split()[1])/1024/1000)[0:4]
            TempFreimem=str(int(line.split()[3])/1024/1000)[0:4]
            Hauptmem = TempHauptmem.replace("."," komma ")
            Freimem = TempFreimem.replace("."," komma ")
            return(Hauptmem, Freimem)
            
def rechnen(wert1_value,wert2,wert2_value,wert3_value):
    w1 = str(wert1_value)
    w3 = str(wert3_value)
    sprache = "Nicht verstanden"
    #print("wert1_value",wert1_value,"wert2",wert2,wert2_value,"wert3_value",wert3_value)    
    if wert2 == "ADD":
        ergebnis = int(wert1_value)+int(wert3_value)
        sprache = w1 +" "+ wert2_value +" "+ w3+" ist "+str(ergebnis)
    elif wert2 =="MULTIPLI":
        ergebnis = int(wert1_value)*int(wert3_value)
        sprache = w1 +" "+ wert2_value +" "+ w3+" ist "+str(ergebnis)
    elif wert2 =="SUBTRACT":
        ergebnis = int(wert1_value)-int(wert3_value)
        sprache = w1 +" "+ wert2_value +" "+ w3+" ist "+str(ergebnis)
    elif wert2 =="DIVIDE":
        if wert3_value == 0:
            sprache = "Durch null darf man nicht teilen"
        else:    
                       
            tempergebnis = str(int(wert1_value)/int(wert3_value))
            ergebnis = tempergebnis.replace("."," komma ")
            sprache = w1 +" "+ wert2_value +" "+ w3+" ist "+ergebnis
        
    sprachausgabe('"%s"' %sprache)
           
           
def licht(wert1,wert1_value):
    print("wert1",wert1,"wert1_value",wert1_value)

    if wert1 == "AN":
    
       sysswitch = "curl -s 'http://192.168.5.230/cm?user=admin&password=trailer&cmnd=Power%20on'"
    elif wert1 == "AUS":
        sysswitch = "curl -s 'http://192.168.5.230/cm?user=admin&password=trailer&cmnd=Power%20off'"
    sprache=globs.speaker+" ich soll das Licht "+wert1+" machen"
    sprachausgabe('"%s"' %sprache)
           
    #print("Satz: ",syssentence) 
    subprocess.run(sysswitch,shell=True,stdout=subprocess.DEVNULL)
            
def sound_initialize():       # im tmp Verzeichnis die entsprechende asound lesen
     #print("Bin jetzt hier")
    syssentence = "/usr/sbin/alsactl --file /usr/local/intent/asound.state restore"
    subprocess.run(syssentence,shell=True,stdout=subprocess.DEVNULL)
    
def publish(topic,msg):

     #result=mqttpublish.single('hermes/tts/say', payload=json.dumps({'text': msg,'siteId': 'default', 'modelId': 'default'}))
     print("Msg: mylib.py publish()",msg," Topic: ",topic)

     result=mqttpublish.single(topic,payload=msg )
     #print("Ergebnis: ",result)
       


        