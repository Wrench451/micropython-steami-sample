# Temperature Reading Script with Bluetooth (AIoBLE)

This script allows you to scan for a specific Bluetooth Low Energy (BLE) device, connect to it, and read temperature data from a compatible sensor using the `Environmental Sensing` service (UUID: `0x181A`). It uses the `aioble` library to interact with BLE devices.

## Features

- Scans for a BLE sensor with a filtered MAC address.
- Connects to the sensor and accesses the `Environmental Sensing` service (UUID: `0x181A`).
- Reads the temperature characteristic (UUID: `0x2A6E`) and displays the temperature in Celsius.
- The sensor name is dynamically generated from the MAC address if no name is provided by the device.

## Prerequisites

- A Python environment compatible with the `aioble` library.
- A BLE sensor that supports the `Environmental Sensing` service and temperature characteristic.
- A Bluetooth adapter that supports BLE.

## Installation

Before running the script, make sure the `aioble` library is installed. You can find it in the official MicroPython repository: 

[AIoBLE - MicroPython Bluetooth Library](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble/aioble)

If you're using MicroPython, you can install the library from the MicroPython lib:

```
import upip
upip.install('micropython-aioble')
```

## How It Works

### 1. Scanning and Connecting

The script starts by scanning for BLE devices for 5 seconds. When it detects a device with the MAC address you specify, it attempts to connect to it.

### 2. Accessing Services

Once connected, the script searches for the `Environmental Sensing` service (`UUID: 0x181A`) and the temperature characteristic (`UUID: 0x2A6E`).

### 3. Reading Temperature

Once the temperature characteristic is found, the script reads the temperature value. The temperature is decoded using the appropriate struct format (`<h`), and then displayed in Celsius.

### 4. Repeated Readings

The script reads the temperature every 2 seconds during the connection period and displays the read value each cycle.

## Running the Script

To run this script, simply execute it with Python. If you're using MicroPython, you can also run this script on a MicroPython-compatible board.

```bash
python script.py
```

### Example Output

Here is an example of the output when the script is running correctly:

```
---Start Scan---
MAC: A4:C1:38:3F:19:D6
RSSI : -67
Raw Payload : b'\x02\x01\x06\x0e\x16\xd2\xfc@\x00\x85\x01_\x02\x05\x08\x03\r\x17'
Sensor Name : ATC_3F19D6
-> Connecting to b'\xa4\xc18?\x19\xd6'
-> Connected to Device(ADDR_PUBLIC, a4:c1:38:3f:19:d6, CONNECTED)
-> Service and Characteristic found
Temperature: 20.54
Temperature: 20.53
Temperature: 20.55
...
```

## Source

This script is based on the examples provided by the `aioble` library in MicroPython. You can view more examples in the following repository:

[AIoBLE - MicroPython Examples](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble/examples)