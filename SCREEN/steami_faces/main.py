import framebuf
from machine import SPI, Pin
import ssd1327
from time import sleep

# Initialisation de l'affichage et du SPI
spi = SPI(1)
dc = Pin("DATA_COMMAND_DISPLAY")
res = Pin("RST_DISPLAY")
cs = Pin("CS_DISPLAY")

display = ssd1327.WS_OLED_128X128_SPI(spi, dc, res, cs)

scaled = 104
factor = scaled // 8 

Smileys = {
    "Eye_hatHat": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b01000010,
        0b10100101,
        0b00000000,
        0b00000000,
        0b00000000,
    ],
    "Eye_heart": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b10100101,
        0b11100111,
        0b01000010,
        0b00000000,
        0b00000000,
    ],
    "Eye_cross": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b10100101,
        0b01000010,
        0b10100101,
        0b00000000,
        0b00000000,
    ],
    "Eye_close": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b11100111,
        0b00000000,
        0b00000000,
        0b00000000,
    ],
    "Eye_big": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b11100111,
        0b11100111,
        0b11100111,
        0b00000000,
        0b00000000,
    ],
    "Eye_scare": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b11100111,
        0b10100101,
        0b11100111,
        0b00000000,
        0b00000000,
    ],
    "Eye_small": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b01000010,
        0b00000000,
        0b00000000,
        0b00000000,
    ],
    "Eye_long": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b01000010,
        0b01000010,
        0b00000000,
        0b00000000,
        0b00000000,
    ],
    "Eye_pissed": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b11100111,
        0b01000010,
        0b00000000,
        0b00000000,
        0b00000000,
    ],
    "Eye_cry": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b11100111,
        0b01000010,
        0b01000010,
        0b01000010,
        0b00000000,
    ],
    "Eye_sideHat": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b10000001,
        0b01000010,
        0b10000001,
        0b00000000,
        0b00000000,
    ],
    "Faces_happy": [
        0b00000000,
        0b00000000,
        0b01000010,
        0b01000010,
        0b00000000,
        0b01000010,
        0b00111100,
        0b00000000,
    ],
    "Faces_neutral": [
        0b00000000,
        0b00000000,
        0b01000010,
        0b01000010,
        0b00000000,
        0b00000000,
        0b01111110,
        0b00000000,
    ],
    "Faces_sad": [
        0b00000000,
        0b00000000,
        0b01000010,
        0b01000010,
        0b00000000,
        0b00111100,
        0b01000010,
        0b00000000,
    ],
    "Faces_schocked": [
        0b00000000,
        0b00000000,
        0b01000010,
        0b01000010,
        0b00000000,
        0b00111100,
        0b01111110,
        0b00000000,
    ],
    "Faces_bigSmile": [
        0b00000000,
        0b00000000,
        0b01000010,
        0b01000010,
        0b00000000,
        0b01111110,
        0b00111100,
        0b00000000,
    ],
    "Faces_wink": [
        0b00000000,
        0b00000000,
        0b01000000,
        0b01000011,
        0b00000000,
        0b00000010,
        0b00000100,
        0b00111000,
    ],
    "Faces_cry": [
        0b00000000,
        0b00000000,
        0b11000011,
        0b01000010,
        0b01000010,
        0b00011000,
        0b00100100,
        0b00000000,
    ],
    "Faces_tongue": [
        0b00000000,
        0b00000000,
        0b01000010,
        0b01000010,
        0b00000000,
        0b01111110,
        0b00011000,
        0b00011000,
    ],
    "small_heart": [
        0b00000000,
        0b00000000,
        0b00000000,
        0b00100100,
        0b00111100,
        0b00011000,
        0b00000000,
        0b00000000,
    ],
    
}


for smiley_name, bitmap in Smileys.items():
    print(f"-> {smiley_name}")
    if smiley_name == "_":
        bitmap_bytearray = bytearray(bitmap)
        STeaMi_buf = framebuf.FrameBuffer(bitmap_bytearray, 8, 8, framebuf.MONO_HLSB) 

        scaled_bitmap = bytearray((scaled * scaled) // 8)
        scaled_buf = framebuf.FrameBuffer(scaled_bitmap, scaled, scaled, framebuf.MONO_HLSB)

        for y in range(8):
            for x in range(8):
                if STeaMi_buf.pixel(x, y):
                    scaled_buf.fill_rect(x * factor, y * factor, factor, factor, 255)  

        display.fill(0) 
        display.framebuf.blit(scaled_buf, 12, 12, 255) 
        display.show()  

        sleep(2)
