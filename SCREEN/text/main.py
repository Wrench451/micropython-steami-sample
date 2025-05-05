from time import sleep
import ssd1327
from machine import SPI, Pin

spi = SPI(1)
dc = Pin("DATA_COMMAND_DISPLAY")
res = Pin("RST_DISPLAY")
cs = Pin("CS_DISPLAY")

display = ssd1327.WS_OLED_128X128_SPI(spi, dc, res, cs)

display.fill(0)
display.text("Hello World", 20, 40)
display.text("This is a test", 10, 70)
display.show()