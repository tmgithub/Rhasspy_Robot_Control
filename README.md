# Rhasspy_Robot_Control

## Inhalt



* [General](#General)
* [Hardware](#Hardware)
* [Setup](#Setup)
* [MQtt](#MQtt)
* [Repository](#Repository)
* [Program Sequence](#Program Sequence)

## General <a name="General"></a>
This project controls servo motors of a roboter via offline voice control ( rhasspy ).

## Software
* Raspberryos (opensource)
>```https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2022-04-07/2022-04-04-raspios-bullseye-armhf-lite.img.xz```
* rhasspy ( offline Spracherkennungsprogramm)

## Client Software
* mqtt explorer <br />

## Hardware <a name="Hardware"></a>
Hardware to buy:
* Raspberry Pi 4 4 GByte RAM short RPi
<p align="left"><img src="Bilder/rpi4.jpg" width="150"></p><br />
* ReSpeaker 6 Mic Array for Raspberry Pi
<p align="left"><img src="Bilder/respeaker.jpg" width="150"></p><br />
* PCA9685 16 Kanal 12 Bit PWM Servo driver for Raspberry Pi
<p align="left"><img src="Bilder/pcf.jpg" width="150"></p><br />
* Real Time Clock RTC DS3231 I2C
<p align="left"><img src="Bilder/ds3231.jpg" width="150"></p><br />
* Case with enough space for the HAT
<p align="left"><img src="Bilder/RPI4_CASE_SECURE_01.png" width="150"></p><br />
	
## Setup <a name="Setup"></a>
Set up the  Raspberry Pi's 4 for the offline voice recognition:

**1.** Flash an image to an sd-card ```https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-11-08/2021-10-30-raspios-bullseye-armhf-lite.zip``` <br />
>I used  ```Balena Etcher``` on Mac OS.<br /><br />
Put the SD_Card into the RPI connect a  **HDMI Monitor** and a  **USB-Keyboard** . <br />
Make a physical network connection via ethernet and plug in the power adapter cable. <br />
Login with the user ```pi```and the password ```raspberry```<br />
Be careful the keyboard layout is english **z** instead of **y**. <br />
Give the command  ```sudo passwd ``` so the password for the user root will be set <br />
Change with ```su -``` and the new password to the root user. <br />
Now change the passord for the user pi with ```passwd pi```.

**2.**  Set-up with the command **raspi-config**. <br />
<p align="left"><img src="Bilder/raspi-config1.jpeg" width="150"></p><br />

> As root user with the command ```raspi-config``` under menu item **3 Interface Options**<br />
activate **P2 SSH** and **P5 I2C** .<br />

<p align="left"><img src="Bilder/raspi-config_ssh.jpeg" width="150"></p><br />

> And activate the localisation under menu item 5  **L1 Locale und L2 Timezone und L3 Keyboard **.<br />

<p align="left"><img src="Bilder/raspi-config_hostname.jpeg" width="150"></p><br />

> I changed the hostname with this tool to rhasspy. <br />
> Now i adjusted the config file for ssh ```vi /etc/ssh/sshd_config```.<br />
Change the line with ```PermitRootLogin``` to ```yes```.<br />


**3.**  Make a new start of the RPI ( reboot or init6 on the commandline )

**4.**  Login via ssh ``` ssh -lroot 192.168.XX.XX```  <br />
> Then type in the commands ```apt update``` to update the repository cache and start to install software: <br />
>``` apt-get install python3-pip git mosquitto mosquitto-clients i2c-tools``` <br />
install Docker 
apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
  
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88

echo "deb [arch=armhf signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install docker-ce docker-ce-cli containerd.io

docker run -d -p 12101:12101 --name rhasspy --restart unless-stopped -v "$HOME/.config/rhasspy/profiles:/profiles" -v "/etc/localtime:/etc/localtime:ro" --device /dev/snd:/dev/snd rhasspy/rhasspy --user-profiles /profiles --profile de

change to the folder  <br />

>```cd /usr/local```
   
type following command : <br />

>```git clone https://github.com/tmgithub/Rhasspy_Robot_Control.git```<br />
 
cd into the new folder <br />

>```cd /usr/local/intent```. <br />
   

**7.** Install the pythonlibrarys with pip3: <br />
>```pip3 install paho-mqtt``` install the mosquitto tools for the MQtt<br />
>```pip3 install gpiozero``` install the connection to GPIO of the Raspberry<br />


**10.** Programm als Dienst anlegen der beim booten gestartet wird : <br />
> In dem Verzeichnis ```/usr/local/intent```den Befehl ```python3 -m venv /usr/local/intent``` ausführen.<br />
> Damit wird das virtuelle Environment angelegt.<br />
> In dem Verzeichnis ```/usr/lib/systemd/system```wird die Datei ```reaktion.service``` angelegt oder kopiert. <br />
> Dann wird dem Daemon mit ```systemctl daemon-reload``` die neue Datei bekannt gemacht.<br /><br />
> Mit ```systemctl enable reaktion.service``` wird die Datei zum Ausführen während des Systemstarts eingerichtet.<br />
> ```systemctl start reaktion.service``` startet den Service manuell. Das Stoppen ist dann mit ```systemctl stop reaktion.service``` möglich.<br />
> Man kann mit ```systemctl status reaktion.service``` abrufen ob das Programm läuft.<br /><br />
> Der Inhalt von ```reaktion.service``` :<br /><br />
>>[Unit]<br />
>>Description=Robot_Control   ```Beschreibung des Services```<br />
>>After=network.target<br />
>>[Service]<br />
>>Type=idle ```Der Typ "idle" stellt sicher, dass das Kommando erst ausgeführt wird, wenn alle anderen Dienste geladen sind.``` <br />
>>Restart=on-failure<br />
>>User=root<br />
>>ExecStart=/bin/bash -c 'cd /usr/local/intent/ && source bin/activate && python3 reaktion.py' ```erst wird ein cd in das Verzeichnis ausgeführt```<br />
>>```Dann wird die virtuelle Umgebung gestartet und dann das Programm selbst``` <br />
>>[Install]<br />
>>WantedBy=multi-user.target<br />


## Repository <a name="Repository"></a>

Repository akualisieren :<br />
In dem Verzeichnis /usr/local/intent <br />
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





