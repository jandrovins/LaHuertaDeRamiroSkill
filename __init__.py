from mycroft import MycroftSkill, intent_file_handler
# Required for BME280
import board,digitalio,busio,time,adafruit_bme280
# Required for BH1750
import smbus2
from i2csense.bh1750 import *

class Lahuertaderamiroskill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

        self.BME280_BUS = busio.I2C(board.SCL, board.SDA)
        self.BME280_ADDR = 0x76
        self.BME280 = adafruit_bme280.Adafruit_BME280_I2C(self.BME280_BUS, address=self.BME280_ADDR)
        self.BME280.sea_level_pressure = 1020
        
        self.BH1750_BUS = smbus2.SMBus(1)
        self.BH1750 = BH1750(self.BH1750_BUS)


    def measure_temperature():
        try:
            return self.BME280.temperature
        except Exception as e:
            print("[ERROR]: An error has ocurred getting temperature from BME280:\n\n" + e.message)


    def measure_humidity():
        try:
            return self.BME280.humidity
        except Exception as e:
            print("[ERROR]: An error has ocurred getting humidity from BME280:\n\n" + e.message)


    def measure_pressure():
        try:
            return self.BME280.pressure
        except Exception as e:
            print("[ERROR]: An error has ocurred getting pressure from BME280:\n\n" + e.message)


    def measure_altitude():
        try:
            return self.BME280.altitude
        except Exception as e:
            print("[ERROR]: An error has ocurred getting altitude from BME280:\n\n" + e.message)


    def measure_luminosity():
        try:
            self.BH1750.update()
            if not self.BH1750.sample_ok:
                print("[ERROR]: An error has ocurred getting data from BH1750 - sample is not OK")
            else:
                return self.BH1750.current_state_str
        except Exception as e:
            print("[ERROR]: An error has ocurred getting luminosity from BH1750:\n\n" + e.message)



    @intent_file_handler('lahuertaderamiroskill.intent')
    def handle_lahuertaderamiroskill(self, message):
        self.speak_dialog('lahuertaderamiroskill')

        self.temperature = measure_temperature()
        self.humidity = measure_humidity()
        self.pressure = measure_pressure()
        self.altitude = measure_altitude()
        self.luminosity = measure_luminosity()

        #self.temperature_str = 

        message = message.lower()
        #if "how" in message:

        #elif "temperature" in message:





def create_skill():
    return Lahuertaderamiroskill()
