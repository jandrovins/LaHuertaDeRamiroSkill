#!/home/pi/mycroft-core/.venv/bin/python
import sys
from LaHuertaDeRamiroSkill import Lahuertaderamiroskill

import ubidots_connection

Ramiro = Lahuertaderamiroskill()

Labels = ["Altitude", "Humidity", "Light", "Pressure", "Temperature","Soil_moiture"]

Functions =[Ramiro.measure_altitude(),
        Ramiro.measure_humidity(),
        Ramiro.measure_luminosity(),
        Ramiro.measure_pressure(),
        Ramiro.measure_temperature(),
        Ramiro.measure_soil_moisture()]

for i in range(6):
    ubidots_connection.send_data(Labels[i],Functions[i])
