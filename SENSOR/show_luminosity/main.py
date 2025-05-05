from time import sleep
import ssd1327
from machine import SPI, Pin, I2C
from apds9960 import uAPDS9960 as APDS9960

i2c = I2C(1)
apds = APDS9960(i2c)
apds.enableLightSensor()

spi = SPI(1)
dc = Pin("DATA_COMMAND_DISPLAY")
res = Pin("RST_DISPLAY")
cs = Pin("CS_DISPLAY")

display = ssd1327.WS_OLED_128X128_SPI(spi, dc, res, cs)


while True:
    lum = apds.readAmbientLight()
    print(f"Luminosity: {lum} lux")

    display.fill(0)
    display.text("Luminosity", 28, 20)
    display.text(f"{lum} lux", 20, 50)
    display.show()
    sleep(0.1)