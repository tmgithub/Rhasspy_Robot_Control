# Rhasspy_Robot_Control

## Content

* [General](#General)
* [Hardware](#Hardware)
* [Software](#Software)
* [Setup](#Setup)
* [Repository](#Repository)
* [Program Sequence](#Program_Sequence)

## General <a name="General"></a>
This project controls servo motors of a roboter via offline voice control ( rhasspy ).<br />
It is divided into two parts.<br />
The main part controls the head.<br />
The other parts are controlling themodules
for example the left arm ( it will be realized by a Raspberry pi Zero)

## Software
* Raspberryos (opensource)
>```https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2022-04-07/2022-04-04-raspios-bullseye-armhf-lite.img.xz```
* rhasspy ( offline Spracherkennungsprogramm)
>* eclipse ide
>> this is the place i am working with<br />
>> <br />
>> <p align="left"><img src="Bilder/eclipse.png" width="400"></p><br />
**Client Software**
* mqtt explorer <br />

## Hardware <a name="Hardware"></a>
Hardware to buy:
* Raspberry Pi 4 4 GByte RAM short RPi
<p align="left"><img src="Bilder/rpi4.jpg" width="250"></p><br />
* ReSpeaker 6 Mic Array for Raspberry Pi
<p align="left"><img src="Bilder/respeaker.jpg" width="250"></p><br />
* PCA9685 16 Kanal 12 Bit PWM Servo driver for Raspberry Pi
<p align="left"><img src="Bilder/pcf.jpg" width="250"></p><br />
* Real Time Clock RTC DS3231 I2C
<p align="left"><img src="Bilder/ds3231.jpg" width="250"></p><br />
* Case with enough space for the HAT
<p align="left"><img src="Bilder/RPI4_CASE_SECURE_01.png" width="250"></p><br />
<br />
* this is my case<br />
* and the selfmade case for the respeaker microphone extension.<br />
* you can see the **i2c extender** and the **DS3231** plugged into the **i2c extender**<br />
<p align="left"><img src="Bilder/my_case.jpg" width="250"></p><br />

	
## Setup <a name="Setup"></a>
Set up the  Raspberry Pi's 4 for the offline voice recognition:

**1.** Flash an image to an sd-card <br />
>```https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-11-08/2021-10-30-raspios-bullseye-armhf-lite.zip``` <br />
> I used  ```Balena Etcher``` on Mac OS.<br /><br />
> Put the SD_Card into the RPI connect a  **HDMI Monitor** and a  **USB-Keyboard** . <br />
> Make a **physical network connection** via ethernet and plug in the power adapter cable. <br />
> After the login prompt is blinking on the monitor, login with the user ```pi```and the password ```raspberry```<br />
> Be careful the keyboard layout is english **z** instead of **y**. <br />
> Give the command  ```sudo passwd``` so the password for the user root can be set <br />
> Change with ```su -``` and the new password to the root user. <br />
> Now change the passord for the user pi with ```passwd pi```.

**2.**  Set-up with the command **raspi-config**. <br />
><p align="left"><img src="Bilder/raspi-config1.jpeg" width="250"></p> <br />
> As root user with the command **raspi-config**<br />
> under menu item **3 Interface Options** activate **P2 SSH** and **P5 I2C** .<br />
> <br />
> <p align="left"><img src="Bilder/raspi-config_ssh.jpeg" width="250"></p><br />
> And activate the localisation under menu item **5 L1 Locale und L2 Timezone und L3 Keyboard** . <br />
> <p align="left"><img src="Bilder/raspi-config_hostname.jpeg" width="250"></p><br />
> I changed the hostname with this tool to rhasspy. <br />
> Now i adjusted the config file for ssh ```vi /etc/ssh/sshd_config```.<br />
> Change the line with ```PermitRootLogin``` to ```yes```.<br />


**3.**  Make a new start of the RPI ( reboot or init6 on the commandline )

**4.**  Login via ssh **```ssh -lroot 192.168.XX.XX```**  <br />
> Then type in the commands **```apt update```** to update the repository cache and start to install software: <br />
> <br />
> **```apt-get install python3-pip git mosquitto mosquitto-clients i2c-tools```** <br />
> install **Docker** <br />
> <br />
> ```**apt-get install** apt-transport-https ca-certificates curl gnupg-agent software-properties-common```<br />
> <br />
> ```**curl -fsSL** https://download.docker.com/linux/debian/gpg | sudo apt-key add -```<br />
> <br />
> ```**apt-key** fingerprint 0EBFCD88```<br />
> <br />
> ```**echo** "deb [arch=armhf signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null```<br />
> <br />
> ```apt-get update```<br />
> ```apt-get install docker-ce docker-ce-cli containerd.io```<br />
> <br />
> docker run -d -p 12101:12101 --name rhasspy --restart unless-stopped -v "$HOME/.config/rhasspy/profiles:/profiles" -v "/etc/localtime:/etc/localtime:ro" --device /dev/snd:/dev/snd rhasspy/rhasspy --user-profiles /profiles --profile de
> V
**Now the rhasspy needs some configurations**

change to the folder  <br />

>```cd /usr/local```
   
type following command : <br />

>```git clone https://github.com/tmgithub/Rhasspy_Robot_Control.git```<br />
 
cd into the new folder <br />

>```cd /usr/local/intent```. <br />
   

**5.** Install the pythonlibrarys with pip3: <br />
>```pip3 install paho-mqtt``` install the mosquitto tools for the MQtt<br />
>```pip3 install gpiozero``` install the connection to GPIO of the Raspberry<br />


**6.** Program as a servie wich start at boottime : <br />
> Change to the folder ```/usr/local/intent``` and execute the command ```python3 -m venv /usr/local/intent```.<br />
> The virtual environment would established.<br />
> In the folder ```/usr/lib/systemd/system``` the file ```reaktion.service``` is copied or generated. <br />
> Tell the daemon with ```systemctl daemon-reload``` about the new file.<br /><br />
> with ```systemctl enable reaktion.service``` the file is ready to be used while system starts.<br />
> ```systemctl start reaktion.service``` will start the service manual. The stopping is with the command ```systemctl stop reaktion.service``` possible.<br />
> You can show the status by typing ```systemctl status reaktion.service```.<br /><br />
> The content of the file```reaktion.service``` :<br /><br />
>>[Unit]<br />
>>Description=Robot_Control   ```Descripotion of the Service```<br />
>>After=network.target<br />
>>[Service]<br />
>>Type=idle ```The type idle means the command starts when all other processes are finished.``` <br />
>>Restart=on-failure<br />
>>User=root<br />
>>ExecStart=/bin/bash -c 'cd /usr/local/intent/ && source bin/activate && python3 reaktion.py' ```first cd to the folder```<br />
>>```then the virual env is started``` <br />
>>[Install]<br />
>>WantedBy=multi-user.target<br />


**7.** config Rhasspy <br />

> listening to mqtt <br />
> <p align="left"><img src="Bilder/Rhasspy_MQTT.png" width="150"></p><br />
> <br />
> i use pyaudio for recording the voice<br /><br />
> <p align="left"><img src="Bilder/Rhasspy_audio_recording.png" width="150"></p><br />
> <br />
> my roboter is named kai, i use the wakeword engine **Rhasspy Raven** <br />
> <p align="left"><img src="Bilder/Rhasspy_wake_word.png" width="150"></p><br />
> <br />
> speech to text via kaldi <br />
> <p align="left"><img src="Bilder/Rhasspy_speech_to_text.png" width="150"></p><br />
> <br />
> intent recognition via Fsticuffs <br />
> <p align="left"><img src="Bilder/Rhasspy_intent_recognition.png" width="150"></p><br />
> <br />
> all words were send to mqtt so other programs can listen to them <br />
> <p align="left"><img src="Bilder/Rhasspy_text_to_Speech.png" width="150"></p><br />
> <br />
> the sound is played by aplay ( for example error sound etc.) <br />
> <p align="left"><img src="Bilder/rhasspy_audio_play.png" width="150"></p><br />


## Repository <a name="Repository"></a>

actualize Repository  :<br />
change to folder /usr/local/intent <br />
start the following commands :<br />

```git add -A```<br />
```git commit -m "sync"```<br />
```git pull```<br />
```git push```<br />

the commands  push / pull  needs login.

## Program_Sequence <a name="Program Sequence"></a>

Program Sequence :

>The program reaktion.py will be started  with the following command<br />
>```cd /usr/local/intent/ python3 reaktion.py```<br />
><br />
> **after loading the libraries** the main program start a subprocess<br />
> to speak word:<br />
> >subprocess.Popen(['/usr/bin/python3','/usr/local/intent/hermes_sprachausgabe.py'])<br />
>> time.sleep(4)<br />
>> globs.initialize() ### Globale Variablen initialisieren<br />
>> MY.sound_initialize()<br />











