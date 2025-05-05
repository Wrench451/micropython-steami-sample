# Distance Measurement with OLED Display

This project demonstrates how to measure distance using the VL53L1X Time-of-Flight sensor and display the results on an SSD1327 OLED screen. The code is written in MicroPython and uses SPI and I2C communication protocols.

## Hardware Requirements
- VL53L1X Time-of-Flight distance sensor
- SSD1327 OLED display (128x128 resolution)
- Microcontroller with SPI and I2C support
- Connecting wires

## Software Requirements
- MicroPython firmware installed on the microcontroller
- `ssd1327` library for OLED display
- `vl53l1x` library for the distance sensor

## How It Works
1. The VL53L1X sensor measures the distance to an object in millimeters.
2. The measured distance is printed to the console and displayed on the OLED screen.
3. The display is updated every 0.1 seconds in an infinite loop.

## Connections
- Connect the VL53L1X sensor to the I2C pins of the microcontroller.
- Connect the SSD1327 OLED display to the SPI pins (`DATA_COMMAND_DISPLAY`, `RST_DISPLAY`, `CS_DISPLAY`).

## Usage
1. Flash the MicroPython firmware onto your microcontroller.
2. Install the required libraries (`ssd1327` and `vl53l1x`).
3. Upload the code to the microcontroller.
4. Run the script to start measuring distances and displaying them on the OLED screen.

## Notes
- Ensure the pins in the code match your hardware connections.
- Adjust the display text positions if needed for better alignment.