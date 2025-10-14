import bluetooth
import uasyncio as asyncio
import aioble
import struct
from time import ticks_ms, ticks_diff
from pins import *  # Assure-toi que DISTANCE et display sont bien définis ici

# === Initialisation BLE ===
ble = bluetooth.BLE()
ble.active(True)

device_name = f"STeaMi-A"
print("Device name:", device_name)

# === Paramètres du BLE ===
SCAN_DURATION = 500  # Durée de la recherche en ms
ADV_TIMEOUT = 500  # Durée de l'annonce en ms

# === Données locales et des autres appareils ===
devices_distances = {}  # {device_name: (distance, last_seen_ms)}
forwarded_presence = None

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
    global forwarded_presence
    while True:
        print("BLE Task: Starting scan...")
        async with aioble.scan(SCAN_DURATION, interval_us=30000, window_us=30000, active=True) as scanner:
            print("BLE Task: Scanning...")
            async for result in scanner:
                name = result.name()
                if name and name.startswith("STeaMi") and name != device_name:
                    man_data = extract_manufacturer_data(result.adv_data)
                    if man_data and len(man_data) == 2:
                        distance, = struct.unpack("h", man_data)
                        devices_distances[name] = (distance, ticks_ms())
                        print(f"Received from {name}: {distance} cm")
                    if man_data and len(man_data) == 1 and name.startswith("STeaMi-R"):
                        forwarded_presence_relay, = struct.unpack("b", man_data)
                        devices_distances[name] = (forwarded_presence_relay, ticks_ms())
                        if name.startswith("STeaMi-R2"):
                            forwarded_presence = forwarded_presence_relay
                        print(f"Received presence from {name}: {forwarded_presence_relay}")

        # purge_old_devices()
        await asyncio.sleep_ms(SCAN_DURATION+50)

        if forwarded_presence is not None:
            if forwarded_presence == 0:
                LED_RED.on()
                print("Presence detected within 300 mm !")
            elif forwarded_presence == 1:
                LED_GREEN.on()
                print("Presence detected between 300 mm and 600 mm !")
            elif forwarded_presence == 2:
                LED_BLUE.on()
                print("Presence detected beyond 600 mm !")
            await asyncio.sleep_ms(200)
            LED_RED.off()
            LED_GREEN.off()
            LED_BLUE.off()
            forwarded_presence = None  # Reset after indication

async def display_task():
    while True:
        display.fill(0)

        # Nom de l'appareil + distance locale
        display.text(device_name, text_x_center(device_name), 20, 255)

        # Affichage des appareils les plus récemment vus
        recent_devices = sorted(
            devices_distances.items(),
            key=lambda item: item[1][1],  # tri par last_seen_ms
            reverse=True
        )[:4]

        y = 50
        for name, (dist, _) in recent_devices:
            display.text(f"{name[-4:]}: {dist}", text_x_center("XXXX: XXX"), y, 255)
            y += 10

        display.show()
        await asyncio.sleep(0.2)

# === Programme principal ===

async def main():
    await asyncio.gather(
        ble_task(),
        display_task()
    )

asyncio.run(main())
