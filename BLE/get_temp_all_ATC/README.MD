Sure! Here's a README in English, with a note that the script is not fully finished and can be unstable:

---

# BLE Temperature Sensor Reader (WIP)

This Python script scans for BLE (Bluetooth Low Energy) temperature sensors, connects to them, and reads temperature data using the standard Environmental Sensing Service (UUID 0x181A). It's designed for use with sensors that advertise a specific MAC address prefix.

### ⚠️ **Important Note**
This script is **work-in-progress** and **frequently crashes**. It is not fully stable or production-ready. Use it as a prototype or for experimental purposes only.

---

## Features

- Scans for BLE devices with a MAC address starting with a specific prefix (`A4:C1:38` by default).
- Connects to found devices and reads temperature from the Environmental Sensing Service.
- Parses and displays temperature in degrees Celsius.
- Supports basic error handling for connection issues and timeouts.

---

## Requirements

- Python 3.7+
- `aioble` (BLE library for asyncio)
- `asyncio`
- A BLE adapter compatible with the host system
- BLE temperature sensors supporting Environmental Sensing Service (0x181A)

---

## How to Use

1. Install dependencies (you might need to adjust for your environment):

   ```bash
   pip install aioble
   ```

2. Run the script:

   ```bash
   python your_script_name.py
   ```

3. The script will:
   - Scan for 5 seconds for devices with the specified MAC address prefix.
   - Attempt to connect and read temperature data.
   - Print out the collected data.

---

## Known Issues

- **Frequent Crashes:** The script is not robust and may fail during scanning or connecting.
- **Limited Error Handling:** While there is some basic error catching, many edge cases are not covered.
- **Single Device Focus:** Currently processes only the first matching device found.
- **Blocking Calls:** Some operations might block or cause the script to hang if the BLE device is unresponsive.

---

## To Do / Improvements

- Improve error handling and reconnection logic.
- Support multiple devices in parallel.
- Make scanning and MAC filtering more configurable.
- Add logging and better timeout management.
- Refactor for better readability and modularity.

---

Feel free to test and modify the script, but **expect instability**!

--- 

Let me know if you'd like to refine or expand any part of this!