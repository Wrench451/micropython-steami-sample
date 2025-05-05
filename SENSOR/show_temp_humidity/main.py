from time import sleep
import ssd1327
from machine import SPI, Pin, I2C
from hts221 import HTS221

i2c = I2C(1)
SENSOR = HTS221(i2c)


spi = SPI(1)
dc = Pin("DATA_COMMAND_DISPLAY")
res = Pin("RST_DISPLAY")
cs = Pin("CS_DISPLAY")

display = ssd1327.WS_OLED_128X128_SPI(spi, dc, res, cs)


while True:
    temp = SENSOR.temperature()
    humid = SENSOR.humidity()
    print(f"Temperature: {temp} C")
    print(f"Humidity: {humid} %")

    display.fill(0)
    display.text("SENSORS", 35, 20)
    display.text(f"Temp: {round(temp, 1)} C", 5, 50)
    display.text(f"Humid: {round(humid, 1)} %", 5, 70)
    display.show()
    sleep(0.1)