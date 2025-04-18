Voici ton `README.md` mis à jour pour refléter les derniers changements dans le code, notamment :

- l’ajout du mapping UUID → nom humain,
- une meilleure lisibilité du journal (log formaté),
- la suppression de la mention du fallback ADV (qui n’est plus utilisé directement).

---

```markdown
# BLE Central Device Scanner (MicroPython)

This project implements a Bluetooth Low Energy (BLE) Central role using MicroPython. It scans nearby BLE peripherals, connects to each device, and reads all GATT characteristics found in the first service. It attempts to decode the values (e.g., device name, local name) and prints them in a human-readable format.

---

## 📦 Features

- Scans nearby BLE devices for 10 seconds
- Filters duplicates and stores unique device addresses
- Connects to each discovered device, one-by-one
- Reads all characteristics of the first discovered GATT service
- Automatically decodes standard UUIDs:
  - Example: `0x2A00` → `"Device Name"`, `0x2A04` → `"Preferred Connection Parameters"`
- Automatically decodes characteristic values to readable strings when possible
- Times out and skips devices that do not respond within 5 seconds
- Structured and color-tagged logs for better readability

---

## 🔧 Requirements

- MicroPython board with BLE support (e.g., ESP32, STM32WB55)
- MicroPython firmware with `bluetooth` and `ubluetooth` modules enabled
- `ble_advertising.py` helper module (for parsing advertisement payloads)

---

## 🚀 How to Use

1. Flash the code to your MicroPython-compatible board.
2. Open a serial connection (e.g., `minicom`, `screen`, or Thonny).
3. Reset the board. It will:
   - Start a 10-second BLE scan
   - Print found devices
   - Connect and try to read characteristics from each
   - Display results in a readable format

You should see output like:

```
[SCAN] Found device: 0 b'\xa4\xc18x:d' | RSSI: -70 | Name: ? | Services: []
...
[INFO] Scan complete. Devices found:
  - 0 b'\xa4\xc18x:d' → ?
  - 0 b'fN\xd79\xa7\r' → ?
  ...

[CONNECT] Connecting to 0 b'\xa4\xc18x:d' (?)...
[READ] Characteristic 1/3 | UUID: Preferred Connection Parameters
[CHAR] Handle: 3 → "ATC_783A64"
[READ] Characteristic 2/3 | UUID: Preferred Connection Parameters
[CHAR] Handle: 5 → ""
[READ] Characteristic 3/3 | UUID: Preferred Connection Parameters
[CHAR] Handle: 7 → "10"
[INFO] Disconnected from b'\xa4\xc18x:d'
```

---

## ⚠️ Notes

- Many commercial BLE devices **do not expose** the GATT Device Name (`0x2A00`) or any useful GATT characteristics.
- Most devices do **not advertise** their name in the scan response.
- The characteristic values may sometimes be binary or empty.
- Some devices may require pairing or bonding before access.

---

## 🧪 Recommended Test Peripheral

You can test this code using a simple BLE peripheral that advertises a name and exposes a readable GATT characteristic.  
For example, on another ESP32:

```python
import bluetooth
from ble_advertising import advertising_payload

ble = bluetooth.BLE()
ble.active(True)
payload = advertising_payload(name="ESP32_Test")
ble.gap_advertise(100_000, adv_data=payload)
```

---

## 🧠 Tip

To add support for more UUIDs (e.g., battery level, heart rate), extend the `_UUID_NAMES` dictionary in the code:

```python
_UUID_NAMES = {
    bluetooth.UUID(0x2A00): \"Device Name\",
    bluetooth.UUID(0x2A01): \"Appearance\",
    bluetooth.UUID(0x2A04): \"Preferred Connection Parameters\",
    bluetooth.UUID(0x2AC9): \"Local Name\",
    bluetooth.UUID(0x2A19): \"Battery Level\",  # example
}
```

---

## 📂 License

MIT License — do what you want with it 🚀
```

Souhaite-tu que je le colle aussi dans un fichier `README.md` dans ton projet sur la canvas ?