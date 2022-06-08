
import time
from playsound import playsound
import threading
from datetime import datetime
import playsound

#taking input from user
alarmH = 3
alarmM = 10
amPm = 'am'

print("Waiting for the alarm",alarmH,alarmM,amPm)
if (amPm == "pm"):
     alarmH = alarmH + 12

#Current Date Time
now = datetime.now()

#desired alarm time
later = datetime(2020,5,1,alarmH,alarmM,0)

#calculating the difference between two time
difference = (later - now)

#difference in seconds
total_sec=difference.total_seconds() 

def alarm_func():
    playsound.playsound('audio/alarm.mp3', True)

timer = threading.Timer(total_sec, alarm_func)
timer.start()

#<STELLE>\[(mir|mich|uns)] \[<EINEN>]<WECKER>\[<FAUF>]\[<SEC>]\[<MIN>]\[<HSTD>]\[<STD>]\[<MINSTDSEC>]
