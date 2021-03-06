from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.format import nice_date_time
# Required for BME280
import board
import digitalio
import busio
import time
import adafruit_bme280
# Required for BH1750
import smbus2
from i2csense.bh1750 import *
# Required for MCP3201
import sys
# Required for pump relay
import RPi.GPIO as GPIO
import time
# Required for logging pump activation
from datetime import datetime as dt
# Required for sendig data to Ubidots
from . import ubidots_connection
from .MCP3201 import MCP3201
#from . import Relay
import subprocess
import os


class Lahuertaderamiroskill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

        self.BME280_BUS = busio.I2C(board.SCL, board.SDA)
        self.BME280_ADDR = 0x76
        self.BME280 = adafruit_bme280.Adafruit_BME280_I2C(
            self.BME280_BUS, address=self.BME280_ADDR)
        self.BME280.sea_level_pressure = 1020

        self.BH1750_BUS = smbus2.SMBus(1)
        self.BH1750 = BH1750(self.BH1750_BUS)

        self.MCP3201 = MCP3201(0, 0)

    def string_to_number(self, s):
        dic = {
                "one":1,
                "two":2,
                "three":3,
                "four":4,
                "five":5,
                "six":6,
                "seven":7,
                "eight":8,
                "nine":9,
                "ten":10,
                "eleven":11,
                "twelve":12,
                "thirteen":13,
                "fourteen":14,
                "fifteen":15
                }
        try:
            if type(int(s)) == type(2):
                return int(s)
        except:
            return int(dic[s])

    def measure_temperature(self):
        try:
            return round(self.BME280.temperature,2)
        except Exception as e:
            print(
                "[ERROR]: An error has ocurred getting temperature from BME280:\n\n" + e.message)

    def measure_humidity(self):
        try:
            return round(self.BME280.humidity,2)
        except Exception as e:
            print(
                "[ERROR]: An error has ocurred getting humidity from BME280:\n\n" + e.message)

    def measure_pressure(self):
        try:
            return round(self.BME280.pressure,2)
        except Exception as e:
            print(
                "[ERROR]: An error has ocurred getting pressure from BME280:\n\n" + e.message)

    def measure_altitude(self):
        try:
            return round(self.BME280.altitude, 2)
        except Exception as e:
            print(
                "[ERROR]: An error has ocurred getting altitude from BME280:\n\n" + e.message)

    def measure_luminosity(self):
        try:
            self.BH1750.update()
            if not self.BH1750.sample_ok:
                print(
                    "[ERROR]: An error has ocurred getting data from BH1750 - sample is not OK")
            else:
                return self.BH1750.current_state_str
        except Exception as e:
            print(
                "[ERROR]: An error has ocurred getting luminosity from BH1750:\n\n" + e.message)

    def measure_soil_moisture(self):
        try:
            ADC_output_code = self.MCP3201.readADC_MSB()
            return round((ADC_output_code - 4096) / (1947 - 4096),2)
        
        except Exception as e:
            print(
                "[ERROR]: An error has ocurred getting soil moisture from MCP3201:\n\n"+e.message)

    @intent_file_handler('environment.intent')
    def handle_environment(self, message):
        self.speak_dialog('checking')

        self.temperature = self.measure_temperature()
        self.humidity = self.measure_humidity()
        self.pressure = self.measure_pressure()
        self.altitude = self.measure_altitude()
        self.luminosity = self.measure_luminosity()
        self.soil_moisture = self.measure_soil_moisture()

        self.temperature_str = "the temperature is " + str(self.temperature)
        self.humidity_str = "the humidity is " + str(self.humidity)
        self.pressure_str = "the pressure is " + str(self.pressure)
        self.altitude_str = "the altitude is " + str(self.altitude)
        self.luminosity_str = "the luminosity is " + str(self.luminosity)
        self.soil_moisture_str = "the soil moisture is " + str(self.soil_moisture)

        message = message.data.get('variable').lower()
        if "temperature" in message:
            self.speak(self.temperature_str)
        elif "humidity" in message:
            self.speak(self.humidity_str)
        elif "pressure" in message:
            self.speak(self.pressure_str)
        elif "altitude" in message:
            self.speak(self.altitude_str)
        elif "luminosity" in message:
            self.speak(self.luminosity_str)
        elif "soil" in message:
            self.speak(self.soil_moisture_str)

    @intent_file_handler('activate_pump.intent')
    def handle_activate_pump(self, message):
        self.speak_dialog('activating_pump')
        sleeping_time = self.string_to_number(message.data.get('number'))

        os.system("/opt/mycroft/skills/lahuertaderamiroskill.jandrovins/Relay.py " + str(sleeping_time))


        with open('/home/pi/last_pump_activation.txt','w') as f:
            f.write(dt.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        ubidots_connection.send_data('pump',1)






    @intent_file_handler('all_data.intent')
    def handle_all_data(self, message):
        self.speak_dialog('checking')

        self.temperature = self.measure_temperature()
        self.humidity = self.measure_humidity()
        self.pressure = self.measure_pressure()
        self.altitude = self.measure_altitude()
        self.luminosity = self.measure_luminosity()
        self.soil_moisture = self.measure_soil_moisture()

        self.temperature_str = "the temperature is " + str(self.temperature)
        self.humidity_str = "the humidity is " + str(self.humidity)
        self.pressure_str = "the pressure is " + str(self.pressure)
        self.altitude_str = "the altitude is " + str(self.altitude)
        self.luminosity_str = "the luminosity is " + str(self.luminosity)
        self.soil_moisture_str = "the soil moisture is " + str(self.soil_moisture)

        self.speak(self.temperature_str)
        self.speak(self.humidity)
        self.speak(self.pressure_str)
        self.speak(self.altitude_str)
        self.speak(self.luminosity_str)
        self.speak(self.soil_moisture_str)

    @intent_file_handler('last_pump_activation.intent')
    def handle_last_pump_activation(self, message):
        self.speak_dialog('checking')
        
        with open('/home/pi/last_pump_activation.txt','r') as f:
            date_string = f.readline().strip("\n")
            date_time = (datetime.strptime(date_string,"%d/%m/%Y %H:%M:%S"))
            date_time_parsed_string = nice_date_time(date_time)
            self.speak(date_time_parsed_string)



def create_skill():
    return Lahuertaderamiroskill()
