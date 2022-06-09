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
>```https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2022-04-07/2022-04-04-raspios-bullseye-armhf-lite.img.xz```
* rhasspy ( offline Spracherkennungsprogramm)

## Client Software
* mqtt explorer <br />

	
## Technik <a name="Technik"></a>
Hardware gekauft:
* Raspberry Pi 4 4 GByte RAM Kurzform RPi
<p align="left"><img src="Bilder/rpi4.jpg" width="150"></p><br />
* ReSpeaker 6 Mic Array for Raspberry Pi
<p align="left"><img src="Bilder/respeaker.jpg" width="150"></p><br />
* PCA9685 16 Kanal 12 Bit PWM Servotreiber für Raspberry Pi
<p align="left"><img src="Bilder/pcf.jpg" width="150"></p><br />
* Real Time Clock RTC DS3231 I2C
<p align="left"><img src="Bilder/ds3231.jpg" width="150"></p><br />
* Gehäuse mit Platz für den HAT
<p align="left"><img src="Bilder/RPI4_CASE_SECURE_01.png" width="150"></p><br />





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
Docker installieren
apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
  
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88

echo "deb [arch=armhf signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install docker-ce docker-ce-cli containerd.io

docker run -d -p 12101:12101 --name rhasspy --restart unless-stopped -v "$HOME/.config/rhasspy/profiles:/profiles" -v "/etc/localtime:/etc/localtime:ro" --device /dev/snd:/dev/snd rhasspy/rhasspy --user-profiles /profiles --profile de

dann in das Verzeichnis wechseln <br />

>```cd /usr/local```
   
den folgenden Befehl ausführen : <br />

>```git clone https://gitlab.alogis.com/tm/pialarm.git```<br />
 
in das neu erzeugte Verzeichnis mit <br />

>```cd /usr/local/pialarm/pideps``` <br />
   
wechseln. <br />
   

**7.** Installation der Pythonlibrarys mit pip3: <br />
>```pip3 install paho-mqtt``` Installiert die mosquitto tools für den MQtt<br />
>```pip3 install gpiozero``` Installiert den Zugriff auf das GPIO des Raspberry's<br />
>```pip3 install adafruit-circuitpython-ina219``` Library für den Zugriff auf die Strommesshardware<br />
>```pip3 install python-pushover``` Installiert tools um den Pushover-Server zu erreichen<br />
>```pip3 install pysnmp``` Installiert snmp tools<br />
>```pip3 install bluepy.btle``` Installiert bluetooth Librarys<br />

**8.** Weitere nützliche Software : <br />


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





