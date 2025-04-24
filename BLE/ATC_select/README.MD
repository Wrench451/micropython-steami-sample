# BLE Sensor Scanner and Data Collector

This script is designed to scan for BLE (Bluetooth Low Energy) devices, filter them based on a specific MAC address prefix, and collect temperature and humidity data from compatible sensors. It also allows the user to interactively select devices to connect to using buttons.

## Features

- **BLE Scanning**: Scans for BLE devices within a specified duration and filters them based on a MAC address prefix.
- **Data Decoding**: Decodes temperature and humidity data from the advertisement packets of compatible sensors.
- **Interactive Device Selection**: Allows the user to select devices to connect to using two buttons (`BTN_A` and `BTN_B`).
- **Data Collection**: Collects and stores sensor data, including temperature, humidity, and scan round information.
- **Summary Output**: Displays a summary of the collected data after the scan.

## Requirements

- **MicroPython**: The script is designed to run on MicroPython-compatible devices.
- **aioble Library**: Used for BLE scanning and interaction.
- **Hardware**: A MicroPython-compatible board with BLE support and two buttons connected to pins `A_BUTTON` and `B_BUTTON`.

## Configuration

- `MAC_ADDRESS_FILTER`: The prefix of the MAC address to filter devices (e.g., `"A4:C1:38"`).
- `ROUNDS`: The number of scan rounds to perform.
- `SCAN_DURATION`: The duration of each scan round in milliseconds.

## How It Works

1. **BLE Scanning**:
   - The script scans for BLE devices for the specified duration.
   - Filters devices based on the `MAC_ADDRESS_FILTER`.
   - Displays the MAC address and name of the detected devices.

2. **Interactive Device Selection**:
   - The user is prompted to select devices using buttons:
     - Press `BTN_A` to select a device.
     - Press `BTN_B` to skip a device.

3. **Data Collection**:
   - For each selected device, the script decodes temperature and humidity data from the advertisement packets.
   - Stores the data in the `collected_data` list.

4. **Summary**:
   - After the scan, the script prints a summary of the collected data, including:
     - Sensor name
     - Temperature (°C)
     - Humidity (%)
     - Scan round number

## Functions

- `_decode_humidity(data)`: Decodes humidity data from the advertisement packet.
- `_decode_temperature(data)`: Decodes temperature data from the advertisement packet.
- `_decode_name(addr)`: Generates a sensor name based on the MAC address.
- `scan_ble()`: Scans for BLE devices and filters them based on the MAC address prefix.
- `wait_for_button_press()`: Waits for a button press (`BTN_A` or `BTN_B`).
- `select_device()`: Allows the user to select devices interactively.
- `main()`: Collects data from the selected devices.

## Usage

1. Connect the hardware (MicroPython board with BLE support and buttons).
2. Configure the script parameters (`MAC_ADDRESS_FILTER`, `ROUNDS`, `SCAN_DURATION`).
3. Run the script on the MicroPython board.
4. Follow the prompts to select devices and view the collected data.

## Example Output

```
--- Scanning for BLE devices... ---
Found device: A4:C1:38:XX:XX:XX, Name: ATC_XXXXXX
Select a device to connect to (A : yes / B : no ):
1: ATC_XXXXXX
Selected
---Starting Scan With Filter A4:C1:38---
==> Found sensor name : ATC_XXXXXX
Temperature : 23.45
Humidity : 45.67
--- Récapitulatif des données collectées ---
Capteur: ATC_XXXXXX, Température: 23.45 °C, Humidité : 45.67, Scan Round: 0
```