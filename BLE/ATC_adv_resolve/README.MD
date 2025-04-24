# ATC_adv_resolve

This script scans nearby Bluetooth Low Energy (BLE) devices, filters ATC sensors based on their MAC address, and collects temperature and humidity data.

## Features

- Scans nearby BLE devices.
- Filters devices whose MAC address starts with a specific prefix (default: `A4:C1:38`).
- Decodes humidity and temperature data from BLE advertisement packets.
- Generates a sensor name based on the MAC address.
- Displays collected data for each detected sensor.

## Requirements

- MicroPython with the following libraries:
  - `aioble`
  - `asyncio`
  - `bluetooth`
  - `struct`

## Usage

1. Ensure your MicroPython environment includes the required libraries.
2. Modify the `MAC_ADDRESS_FILTER` variable if you want to use a different MAC address prefix for filtering sensors.
3. Run the script to start scanning and collecting data.

## Code Structure

- **`_decode_humidity(data)`**: Decodes humidity data from BLE advertisement packets.
- **`_decode_temperature(data)`**: Decodes temperature data from BLE advertisement packets.
- **`generate_name_from_mac(addr)`**: Generates a sensor name based on the MAC address.
- **`main()`**: Main function that performs BLE scanning, filters sensors, and collects data.

## Limitations

- The script assumes BLE advertisement packets have a minimum length of 17 bytes.
- The MAC address prefix is hardcoded and must be manually updated if needed.