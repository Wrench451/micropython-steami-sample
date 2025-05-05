# OLED Display Example

This is a simple Python script demonstrating how to use an SSD1327-based OLED display with a microcontroller. The script initializes the display using SPI communication and displays some text on the screen.

## Requirements

- A microcontroller with SPI support.
- An SSD1327-based OLED display.
- The `ssd1327` library for controlling the display.
- The `machine` module for hardware pin control.

## How It Works

1. The script initializes the SPI interface and configures the necessary pins (`DATA_COMMAND_DISPLAY`, `RST_DISPLAY`, and `CS_DISPLAY`).
2. It creates an instance of the `WS_OLED_128X128_SPI` class to control the 128x128 OLED display.
3. The display is cleared using `fill(0)`.
4. Two lines of text are written to the display at specified coordinates using the `text()` method.
5. The `show()` method updates the display to render the text.

## Example Output

The OLED display will show:
