#!/home/pi/mycroft-core/.venv/bin/python

import RPi.GPIO as GPIO
import time
from sys import argv



def last_activate_pump():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    PIN=40

    GPIO.setup(40,GPIO.OUT)
    GPIO.output(40,GPIO.HIGH)

    GPIO.output(40, GPIO.LOW)
    #print (argv[1])
    #print (argv[0])
    #print("Is on")
    time.sleep(int(argv[1]))
    GPIO.output(40,GPIO.HIGH)
    #print("OFF")
    #time.sleep(3)

    GPIO.cleanup()
    #print("Clean up... DONE")
last_activate_pump()
