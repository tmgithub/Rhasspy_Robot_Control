# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Example that rotates servos on every channel to 180 and then back to 0."""
import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
#print("Anzahl Servos: ",len(kit.servo))
#for i in range(len(kit.servo)):  # pylint: disable=consider-using-enumerate
while True:
    
    kit.servo[0].angle = 178 #Mfinger gestreckt
    time.sleep(1)
    #kit.servo[1].angle = 46
    kit.servo[2].angle = 178
    time.sleep(1)
    kit.servo[3].angle = 46
    
    time.sleep(1)
    kit.servo[0].angle = 46 #Mfinger gestreckt
    #kit.servo[1].angle = 178
    kit.servo[2].angle = 46
    kit.servo[3].angle = 178
    #kit.servo[0].angle = 45
    #kit.servo[1].angle = 180
    #time.sleep(1)
    #kit.servo[1].angle = 45
    #kit.servo[2].angle = 180
    #time.sleep(1)
    #kit.servo[2].angle = 45
    #kit.servo[3].angle = 180
    #time.sleep(1)
    #kit.servo[3].angle = 45
    time.sleep(1)
