# BLE Central Device Scanner (MicroPython)

This project implements a Bluetooth Low Energy (BLE) Central role using MicroPython. It scans nearby BLE peripherals, attempts to connect to each one, and tries to read the device name using both advertisement data and the GATT Generic Access service.

## 📦 Features

- Scans for nearby BLE devices for 10 seconds.
- Filters out duplicate devices during scanning.
- Connects to each discovered device one-by-one.
- Attempts to read the device name:
  - First via GATT (characteristic `0x2A00` in service `0x1800`)
  - Falls back to the advertised name (ADV) if GATT is unavailable.
- Skips unresponsive devices after a 5-second timeout.
- Logs connection and disconnection events for each device.

## 🔧 Requirements

- MicroPython board with BLE support (e.g., ESP32, STM32WB55)
- MicroPython firmware with `bluetooth` and `ubluetooth` modules enabled
- `ble_advertising.py` helper module (for parsing advertisement payloads)

## 🚀 How to Use

1. Flash the code to your MicroPython-compatible device.
2. Open a serial connection (e.g., via `minicom`, `screen`, or Thonny).
3. Reset the board. It will:
   - Scan for devices
   - Attempt connections
   - Print detected names or fallbacks

You should see output like:

```
Scan complete. Found devices:
- 0 b'...'

Connecting to 0 b'...' (?)
[GATT] 0 b'...': MyBLE_Device
...
All devices tested.
```

## ⚠️ Notes

- Many commercial BLE devices do **not expose** the GATT Device Name characteristic (`0x2A00`). This is expected behavior.
- Some devices do **not include** a name in their advertisement data (`adv_data`).
- For testing, use another ESP32 or a custom BLE device (e.g., via nRF Connect) that advertises a name.

## 🧪 Recommended Test Peripheral

You can test this code using a simple BLE peripheral that advertises a name. For example, on another ESP32:

```python
import bluetooth
from ble_advertising import advertising_payload

ble = bluetooth.BLE()
ble.active(True)
payload = advertising_payload(name="ESP32_Test")
ble.gap_advertise(100_000, adv_data=payload)
```