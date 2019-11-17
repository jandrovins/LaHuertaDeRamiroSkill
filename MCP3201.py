import spidev
from time import sleep

class MCP3201(object):

    def __init__(self, SPI_BUS, CE_PIN):
     
        if SPI_BUS not in [0,1]:
            raise ValueError('Wrong SPI-BUS:{0} setting (use 0 or 1)!'.format(SPI_BUS))
        if CE_PIN not in [0,1]:
            raise ValueError('wrong CE-setting: {0} setting (use 0 for CEO or 1 for CE1)!'.format(CE_PIN))
        self._spi = spidev.SpiDev()
        self._spi.open(SPI_BUS, CE_PIN)
        self._spi.max_speed_hz = 976000
        pass

    def readADC_MSB(self):

        bytes_received= self._spi.xfer2([0x00,0x00])

        MSB_1 = bytes_received[1]
        MSB_1 = MSB_1 >> 1 

        MSB_0 = bytes_received[0] & 0b00011111
        MSB_0 = MSB_0 << 7

        return MSB_0 + MSB_1

    def readADC_LSB(self):
        
        bytes_received = self._spi.xfer2([0x00,0x00,0x00,0x00])

        LSB_0 = bytes_received[1] & 0b00000011
        LSB_0 = bin(LSB_0)[2:].zfill(2)

        LSB_1 = bytes_received[2]
        LSB_1 = bin(LSB_1)[2:].zfill(8)

        LSB_2 = bytes_received[3]
        LSB_2 = bin(LSB_2)[2:].zfill(8)
        LSB_2 = LSB_2[0:2]

        LSB = LSB_0 + LSB_1 + LSB_2

        LSB = LSB[::-1]
        return int(LSB,base=2)

    def convert_to_voltage(self, adc_output, VREF=3.3):
        return adc_output * (VREF / (2**12-1))


if __name__ == '__main__' :
    SPI_bus = 0
    CE = 0
    MCP3201 = MCP3201(SPI_bus, CE)

    try:
        while True:
            ADC_output_code = MCP3201.readADC_MSB()
            ADC_voltage = MCP3201.convert_to_voltage(ADC_output_code)
            print("MCP3210 output code (MSB-mode): %d"% ADC_output_code)
            print("MCP3210 voltage: %0.2f V" % ADC_voltage)

            sleep(0.1)

            ADC_output_code = MCP3201.readADC_LSB()
            ADC_voltage = MCP3201.convert_to_voltage(ADC_output_code)
            print("MCP3201 output code (LSB-mode): %d" % ADC_output_code)          
            print("MCP3201 voltage: %0.2f V" % ADC_voltage)
            print()


            sleep(1)

    except (KeyboardInterrupt):
        print('\n',"Exit on Ctrl-C: Good bye!" )

    except:
        print("Other error occurred!")
        
        raise

    finally: 
        print()
