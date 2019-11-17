#!/home/pi/mycroft-core/.venv/bin/python

from datetime import datetime as dt
import RPi.GPIO as GPIO
import time
from . import ubidots_connection

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.OUT)

GPIO.output(40,GPIO.LOW)
time.sleep(10)
GPIO.output(40,GPIO.HIGH)

GPIO.cleanup()
with open('/home/pi/last_pump_activation.txt','w') as f:
    f.write(dt.now().strftime("%d/%m/%Y %H:%M:%S"))

ubidots_connection.send_data('Pump',1)
