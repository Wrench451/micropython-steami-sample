# Sensor Display with HTS221 and SSD1327

This project demonstrates how to use an HTS221 temperature and humidity sensor with an SSD1327 OLED display to show real-time sensor readings.

## Features

- Reads temperature and humidity data from the HTS221 sensor.
- Displays the sensor data on a 128x128 OLED screen using the SSD1327 driver.
- Updates the display in real-time.

## Requirements

- Microcontroller with SPI and I2C support.
- HTS221 temperature and humidity sensor.
- SSD1327-based 128x128 OLED display.
- MicroPython or CircuitPython environment.

## How It Works

1. The HTS221 sensor is connected via I2C to read temperature and humidity.
2. The SSD1327 OLED display is connected via SPI to show the sensor data.
3. The program continuously updates the display with the latest sensor readings.

## Usage

1. Connect the HTS221 sensor and SSD1327 display to your microcontroller.
2. Update the pin definitions (`DATA_COMMAND_DISPLAY`, `RST_DISPLAY`, `CS_DISPLAY`) in the code to match your setup.
3. Upload the code to your microcontroller and run it.
4. The OLED display will show the temperature and humidity readings in real-time.

## Dependencies

- `ssd1327` library for the OLED display.
- `hts221` library for the sensor.

## Example Output
