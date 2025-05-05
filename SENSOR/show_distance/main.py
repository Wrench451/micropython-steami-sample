from time import sleep
import ssd1327
from machine import SPI, Pin, I2C
from vl53l1x import VL53L1X
i2c = I2C(1)

DISTANCE = VL53L1X(i2c)



spi = SPI(1)
dc = Pin("DATA_COMMAND_DISPLAY")
res = Pin("RST_DISPLAY")
cs = Pin("CS_DISPLAY")

display = ssd1327.WS_OLED_128X128_SPI(spi, dc, res, cs)


while True:
    dist = DISTANCE.read()
    print(f"Distance: {dist} mm")

    display.fill(0)
    display.text("Distance", 35, 20)
    display.text(f"{dist} mm", 40, 70)
    display.show()
    sleep(0.1)