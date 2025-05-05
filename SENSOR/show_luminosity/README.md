# Luminosity Sensor with OLED Display

This project demonstrates how to use an APDS9960 ambient light sensor to measure luminosity and display the readings on an SSD1327 OLED screen. The code is written in MicroPython and is designed to run on microcontrollers.

## Features

- Reads ambient light levels using the APDS9960 sensor.
- Displays the luminosity readings on a 128x128 OLED screen (SSD1327).
- Updates the display in real-time.

## Requirements

- Microcontroller with MicroPython support.
- APDS9960 ambient light sensor.
- SSD1327-based 128x128 OLED display.
- SPI and I2C interfaces.
- Required libraries:
    - `ssd1327` for OLED display control.
    - `apds9960` for the light sensor.