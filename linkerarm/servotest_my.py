# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
 
# Import the PCA9685 module.
#import Adafruit_PCA9685
from adafruit_servokit import ServoKit
 
kit = ServoKit(channels=16)


#print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    kit.servo[0].angle = 90
    time.sleep(1)
    kit.servo[0].angle = 0
#kit.continuous_servo[1].throttle = 0

global bereits_initiiert
bereits_initiiert = 0
#import platform
 
# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)
 
# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)



# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
 
# Configure min and max servo pulse lengths
servo_min = 250  # Min pulse length out of 4096
servo_max = 500  # Max pulse length out of 4096
 
# Helper function to make setting a servo pulse width simpler.
#def set_servo_pulse(channel, pulse):
 #   pulse_length = 1000000    # 1,000,000 us per second
 #   pulse_length //= 60       # 60 Hz
 #   print('{0}us per period'.format(pulse_length))
 #   pulse_length //= 4096     # 12 bits of resolution
 #   print('{0}us per bit'.format(pulse_length))
 #   pulse *= 1000
 #   pulse //= pulse_length
 #   pwm.set_pwm(channel, 0, pulse)
 
# Set frequency to 60hz, good for servos.
# pwm.set_pwm_freq(60)#
#def move_servo(channel, pulse, slow):
#    global bereits_initiiert
#    print(pulse,slow)
#    #print("Initiert: ", bereits_initiiert)
#    if bereits_initiiert == 0:
#       initialize_servoboard()
#    try:
#       servopos=int(read_servopos(channel))
#       npulse = servopos - pulse
#       if npulse < 0:
#          step = 5 
#       elif npulse > 0: 
#          step = -5
#       elif npulse == 0:
#          step = 1  
#       if slow == "True":
#       #     print(pulse,  servopos, step)
#            for i in range(servopos, pulse+step, step):
#           #for i in range(pulse, servopos, step):
##             print(pulse, servopos, step, i)
#             pwm.set_pwm(channel, 0, i)
#             write_servopos(channel,i)
#       #      print("after pwm")
#             time.sleep(.05)
#       else:
#       #   print("Else_slow: ") 
#          pwm.set_pwm(channel, 0, pulse)
#          #print("Hier: ",pulse,slow)
#          write_servopos(channel,pulse)
#
#    except Exception as e:
#    #   print(e)
#       bereits_initiiert=0
#       pass

#def initialize_servoboard():
#    global bereits_initiiert
#    global pwm 
#    #print("Init")
#    try:
#        # Alternatively specify a different address and/or bus:
#        pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
#        #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=3)
#        # Set frequency to 60hz, good for servos.
#        pwm.set_pwm_freq(60)
##        pwm.set_pwm(channel, 0, 375)
#        bereits_initiiert=1
#    except Exception as e:
#        bereits_initiiert=0
#        print(e)
#    #print("Init: ", bereits_initiiert)
#initialize_servoboard()
#print('Moving servo on channel 0, press Ctrl-C to quit...')
#while True:
#    # Move servo on channel O between extremes.
##    #pwm.set_pwm(0, 0, servo_min)
#    #print("Zfinger")
#    #time.sleep(1)
#    #pwm.set_pwm(0, 0, servo_max)
#    pwm.set_pwm(0, 0, servo_min)
#    print("Mfinger") 
#    time.sleep(1)
#    pwm.set_pwm(0, 0, servo_max)
#    #pwm.set_pwm(2, 0, servo_min)
#    #print("Ringfinger")
#    #time.sleep(1)
#    #pwm.set_pwm(2, 0, servo_max)
#    #pwm.set_pwm(3, 0, servo_min)
#    #print("Kleinerfinger")
#    #time.sleep(1)
#    #pwm.set_pwm(3, 0, servo_max)
#    #pwm.set_pwm(4, 0, servo_min)
#    #time.sleep(1)
#    #pwm.set_pwm(4, 0, servo_max)
#    
#   # 