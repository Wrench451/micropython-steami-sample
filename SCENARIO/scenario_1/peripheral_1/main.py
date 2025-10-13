import bluetooth
import uasyncio as asyncio
import aioble
import struct
from time import ticks_ms, ticks_diff
from pins import *  # Assure-toi que DISTANCE et display sont bien définis ici

# === Initialisation BLE ===
ble = bluetooth.BLE()
ble.active(True)

# mac_bytes = ble.config('mac')[1]
# mac_suffix = ''.join(f'{b:02X}' for b in mac_bytes[-2:])
device_name = f"STeaMi-S" #-{mac_suffix}"
print("Device name:", device_name)

# === Paramètres du BLE ===
SCAN_DURATION = 3_000  # Durée de la recherche en ms
ADV_TIMEOUT = 1_000  # Durée de l'annonce en ms

# === Données locales et des autres appareils ===
local_distance = 0
devices_distances = {}  # {device_name: (distance, last_seen_ms)}

# === Fonctions auxiliaires ===
def advertising_payload(name=None, manufacturer_data=None):
    payload = bytearray()
    if name:
        name_bytes = name.encode()
        payload += bytes((len(name_bytes) + 1, 0x09)) + name_bytes
    if manufacturer_data:
        payload += bytes((len(manufacturer_data) + 1, 0xFF)) + manufacturer_data
    return payload

def extract_manufacturer_data(adv_bytes):
    i = 0
    while i < len(adv_bytes):
        length = adv_bytes[i]
        if length == 0:
            break
        type_ = adv_bytes[i + 1]
        if type_ == 0xFF:
            return adv_bytes[i + 2 : i + 1 + length]
        i += 1 + length
    return None

def text_x_center(text):
    return max((128 - len(text) * 8) // 2, 0)

# === Tâches ===
async def ble_task():
    while True:
        print("BLE Task: Advertising...")
        man_data = struct.pack("h", local_distance)
        adv_payload = advertising_payload(name=device_name, manufacturer_data=man_data)
        try:
            await aioble.advertise(
                interval_us=150_000,
                adv_data=adv_payload,
                connectable=False,
                timeout_ms=ADV_TIMEOUT
            )
            print("Advertisement done.")
        except asyncio.TimeoutError:
            print("Advertisement timeout (non-connectable).")

        await asyncio.sleep_ms(200)

async def sensor_task():
    global local_distance
    while True:
        local_distance = DISTANCE.read()
        await asyncio.sleep(1)

async def display_task():
    while True:
        display.fill(0)

        # Nom de l'appareil + distance locale
        display.text(device_name, text_x_center(device_name), 60, 255)
        display.text(f"Me: {local_distance}", text_x_center("Me: XXX"), 70, 255)
        display.show()
        await asyncio.sleep(0.2)

# === Programme principal ===

async def main():
    await asyncio.gather(
        sensor_task(),
        ble_task(),
        display_task()
    )

asyncio.run(main())
