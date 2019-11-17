import sys
from LaHuertaDeRamiroSkill import Lahuertaderamiroskill

import ubidots_connection

x = Lahuertaderamiroskill()

NombreLabel = ["Altitude", "Humidity", "Light", "Pressure", "Temperature","Soil_moiture"]

NombreFuncion =[x.measure_altitude(),
        x.measure_humidity(),
        x.measure_luminosity(),
        x.measure_pressure(),
        x.measure_temperature(),
        x.measure_soil_moisture()]

for i in range(6):
    ubidots_connection.send_data(NombreLabel[i],NombreFuncion[i])
