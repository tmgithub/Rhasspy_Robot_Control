# Rhasspy_Robot_Control

## Inhalt



* [Allgemeines](#Allgemeines)
* [Technik](#Technik)
* [Hardware](#Hardware)
* [Setup](#Setup)
* [MQtt](#MQtt)
* [Repository](#Repository)
* [Programmablauf](#Programmablauf)

## Allgemeines <a name="Allgemeines"></a>
Das Projekt soll nach erkannter Sprache Servomotoren ansteuern die einem Roboter gehören  .

## Software
* Raspberryos (opensource)
>```https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-11-08/2021-10-30-raspios-bullseye-armhf-lite.zip```
* rhasspy ( offline Spracherkennungsprogramm)

## Client Software
* mqtt explorer <br />

	
## Technik <a name="Technik"></a>
Hardware gekauft:
* Raspberry Pi 4 4 GByte RAM Kurzform RPi
<p align="center"><img src="Bilder/rpi4.jpg" width="150"></p><br />
<p align="center"><img src="Bilder/respeaker.jpg" width="150"></p><br />
<p align="center"><img src="Bilder/pcf.jpg" width="150"></p><br />
<p align="center"><img src="Bilder/ds3231.jpg" width="150"></p><br />
<p align="center"><img src="Bilder/RPI4_CASE_SECURE_01.png" width="150"></p><br />





## Hardware <a name="Hardware"></a>
	
## Setup <a name="Setup"></a>
Einrichtung des Alarm Pi:

**1.** Zuerst wird eine SD-Card mit dem Image ```https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-11-08/2021-10-30-raspios-bullseye-armhf-lite.zip``` geflasht. <br />
>Programme z.B. ```Balena Etcher``` unter Mac OS.<br />
Die SD_Card wird eingesetzt und ein **HDMI Monitor** und eine **USB-Tastatur** angeschlossen. <br />
Das Netzwerkkabel und das Netzteil wird angeschlossen um die weiteren Schritte zu machen. <br />
Die Anmeldung an der Kommandozeile erfolgt mit dem User ```pi Passwort raspberry```<br />
Achtung Tastatur ist noch Englisch daher bitte **z** statt **y**. <br />
Mit dem Befehl ```sudo passwd ``` wird das root Passwort gesetzt <br />
Dann mit su - (**Achtung Tastatur - ist beim ß**) und dem neuen Passwort zum root user werden. <br />
Als root User das Passwort des Users Pi mit ```passwd pi``` ebenfalls anpassen



**2.**  Einrichtung mit **raspi-config**. <br />
<p align="center"><img src="Bilder/raspi-config1.jpeg" width="150"></p><br />

> Als root User mit dem Kommandozeilen-Tool ```raspi-config``` wird unter dem Menüpunkt **3 Interface Options**<br />
**P2 SSH** und **P5 I2C** aktiviert.<br />

<p align="center"><img src="Bilder/raspi-config_ssh.jpeg" width="150"></p><br />

> Desweiteren können die localisations Options unter Punkt 5 gesetzt werden  L1 Locale und L2 Timezone und L3 Keyboard .<br />

<p align="center"><img src="Bilder/raspi-config_hostname.jpeg" width="150"></p><br />

> Der hostname wird mit dem tool auf pialarm gesetzt. <br />
> Die Konfigdatei für ssh wird mit ```vi /etc/ssh/sshd_config``` angepasst.<br />
Der Wert ```PermitRootLogin``` wird auf yes gesetzt.<br />


**3.**  Dann wird der RPi neu gestartet ( reboot oder init6 auf der Kommandozeile)

**4.**  Nach erfolgreicher Anmeldung per ``` ssh -lroot 192.168.XX.XX```  <br />



**5.** Dann wird ebenfalls auf der Kommandozeile mit ```apt update``` der Repository Cache aktualisiert und folgende Programme werden installiert: <br />
>``` apt-get install python3-pip git mosquitto mosquitto-clients i2c-tools``` <br />

dann in das Verzeichnis wechseln <br />

>```cd /usr/local```
   
den folgenden Befehl ausführen : <br />

>```git clone https://gitlab.alogis.com/tm/pialarm.git```<br />
 
in das neu erzeugte Verzeichnis mit <br />

>```cd /usr/local/pialarm/pideps``` <br />
   
wechseln. <br />

Dort den Befehl : <br />

>```dpkg -i libmbed*.deb``` <br />

ausführen um die fehlenden Abhängigkeiten aufzulösen. <br />
   
Jetzt kann die Funksoftware Pilight installiert werden <br />

>```apt-get install pilight```
   
**6.** Anpassen der Konfigdateien für pilight und mosquitto durch kopieren der Dateien <br />
   
>```cp /usr/local/pialarm/Hilfsdateien/config.json /etc/pilight``` <br />

und <br />

>```cp /usr/local/pialarm/Hilfsdateien/mosquitto.conf /etc/mosquitto/``` <br />

   
Die Dienste müssen nun neu gestartet werden: <br />

>```systemctl restart mosquitto;systemctl status mosquitto``` <br />
   
und <br />

>```systemctl restart pilight;systemctl status pilight``` <br />

**7.** Installation der Pythonlibrarys mit pip3: <br />
>```pip3 install paho-mqtt``` Installiert die mosquitto tools für den MQtt<br />
>```pip3 install gpiozero``` Installiert den Zugriff auf das GPIO des Raspberry's<br />
>```pip3 install adafruit-circuitpython-ina219``` Library für den Zugriff auf die Strommesshardware<br />
>```pip3 install python-pushover``` Installiert tools um den Pushover-Server zu erreichen<br />
>```pip3 install pysnmp``` Installiert snmp tools<br />
>```pip3 install bluepy.btle``` Installiert bluetooth Librarys<br />

**8.** Weitere nützliche Software : <br />

>```apt-get install wavemon mlocate```

**9.** Einrichten des Zugriffs auf den USB-MobileData Stick : <br />
>```ssh -lroot 10.1.1.19``` <br />
> per ssh auf das System einloggen. <br />
> Die Datei ```sshd_config``` anpassen mit  ```vi /etc/ssh/sshd_config```.<br />
> Die Werte <br />
><br />
> ```X11Forwarding yes```<br />
> ```X11UseLocalhost no```<br />
> einfügen und und den Service mit ```service ssh restart``` neu starten<br />
><br />
> Dann mit ```exit``` ausloggen und mit ```ssh -X -lroot 10.1.1.19``` neu anmelden<br />
> wichtig ist das <b>-X</b> da dann die grafische Ausgabe auf eigenen Rechner weitergeleitet wird <br />
> den Firefox aufrufen. Die Ausgabe erfolgt dann auf dem Rechner der den ssh Aufruf gemacht hat.<br />
><br />
> Als Adresse ```http://192.168.8.1``` eingeben. Dann kann man die Qualität des LTE-Signals sehen
<p align="center"><img src="Bilder/Huawei_usbstick.png" width="150"></p><br />

**10.** Programm als Dienst anlegen der beim booten gestartet wird : <br />
> In dem Verzeichnis ```/usr/local/pialarm```den Befehl ```python3 -m venv /usr/local/pialarm``` ausführen.<br />
> Damit wird das virtuelle Environment angelegt.<br />
> In dem Verzeichnis ```/usr/lib/systemd/system```wird die Datei ```pialarm.service``` angelegt oder kopiert. <br />
> Dann wird dem Daemon mit ```systemctl daemon-reload``` die neue Datei bekannt gemacht.<br /><br />
> Mit ```systemctl enable pialarm.service``` wird die Datei zum Ausführen während des Systemstarts eingerichtet.<br />
> ```systemctl start pialarm.service``` startet den Service manuell. Das Stoppen ist dann mit ```systemctl stop pialarm.service``` möglich.<br />
> Man kann mit ```systemctl status pialarm.service``` abrufen ob das Programm läuft.<br /><br />
> Der Inhalt von ```pialarm.service``` :<br /><br />
>>[Unit]<br />
>>Description=Pialarm   ```Beschreibung des Services```<br />
>>After=network.target<br />
>>[Service]<br />
>>Type=idle ```Der Typ "idle" stellt sicher, dass das Kommando erst ausgeführt wird, wenn alle anderen Dienste geladen sind.``` <br />
>>Restart=on-failure<br />
>>User=root<br />
>>ExecStart=/bin/bash -c 'cd /usr/local/pialarm/ && source bin/activate && python3 pialarm_main.py' ```erst wird ein cd in das Verzeichnis ausgeführt```<br />
>>```Dann wird die virtuelle Umgebung gestartet und dann das Programm selbst``` <br />
>>[Install]<br />
>>WantedBy=multi-user.target<br />


## Repository <a name="Repository"></a>

Repository akualisieren :<br />
In dem Verzeichnis /usr/local/pialarm <br />
folgende Kommandos eingeben :<br />

```git add -A```<br />
```git commit -m "sync"```<br />
```git pull```<br />
```git push```<br />

bei den letzten Kommandos push / pull  muss man sich Anmelden.

## Programmablauf <a name="Programmablauf"></a>

Programmablauf :

>Das Pythonprogramm reaktion.py wird mit
```cd /usr/local/intent/ python3 reaktion.py```

gestartet.





