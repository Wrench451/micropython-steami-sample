from micropython import const
import asyncio
import machine
import ubinascii
import aioble
import bluetooth
import struct

from pins import *

# Create a unique device name based on the MAC address
ble = bluetooth.BLE()
ble.active(True)
mac_bytes = ble.config('mac')[1]
mac_suffix = ''.join(f'{b:02X}' for b in mac_bytes[-2:])
device_name = f"STeaMi-{mac_suffix}"
print("Device name:", device_name)

# current distance 
distance = 0

# To navigate the device list
connected_devices = []
devices_index = 0

# display everything on the screen
async def display_task():
    global devices_index, connected_devices, device_name, distance
    while True:
        display.fill(0)
        display.text(device_name, text_x_center_position(device_name), 20, 255)
        display.text(f"{distance}mm", text_x_center_position(f"{distance}mm"), 35, 255)
        display_menu(connected_devices, devices_index)
        display.show()
        await asyncio.sleep(0.1)

# Task to handle the index of the connected devices
async def button_task():
    global devices_index, connected_devices
    while True:
        button = await wait_for_button()
        if button == "A":
            devices_index = (devices_index + 1) % len(connected_devices)
        elif button == "B":
            devices_index = (devices_index - 1) % len(connected_devices)
        elif button == "MENU":
            # Handle menu action here
            pass
        await asyncio.sleep(0.1)

# Define the UUIDs and characteristics for the BLE service
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)
_ADV_INTERVAL_MS = 250_000

temp_service = aioble.Service(_ENV_SENSE_UUID)
temp_characteristic = aioble.Characteristic(
    temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True
)
aioble.register_services(temp_service)

# Function to encode the data 
def _encode_distance(distance_mm):
    return struct.pack("<h", int(distance_mm))

# Task to read the distance from the sensor and update the characteristic
async def sensor_task():
    global distance
    while True:
        distance = DISTANCE.read()
        temp_characteristic.write(_encode_distance(distance), send_update=True)
        await asyncio.sleep_ms(1000)

# Task to handle BLE peripheral functionality
async def peripheral_task(device_name="STeaMi"):
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name=device_name,
            services=[_ENV_SENSE_UUID],
            appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER,
        ) as connection:
            print("Connection from", connection.device)
            try:
                name = connection.device.name()
                if name is None:
                    name = "unknown"
            except:
                name = "unknown"
            connected_devices.append(name)
            print("New device connected:", name)

            await connection.disconnected(timeout_ms=None)
            connected_devices.remove(name)

# Runs the main tasks concurrently
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task(device_name=device_name))
    t3 = asyncio.create_task(display_task())
    t4 = asyncio.create_task(button_task())
    await asyncio.gather(t1, t2, t3,t4)

asyncio.run(main())