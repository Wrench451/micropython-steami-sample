from micropython import const
import asyncio
import machine
import ubinascii
import aioble

from pins import *

# Create a unique device name based on the MAC address
uid = machine.unique_id()
mac_str = ubinascii.hexlify(uid, ':').decode().upper()
mac_suffix = mac_str[-6:].replace(":", "").upper()
device_name = f"STeaMi-{mac_suffix}"

# To navigate the device list
STeaMi_founded = []
STeaMi_index = 0

# display everything on the screen
async def display_task():
    global STeaMi_index, STeaMi_founded, device_name
    while True:
        display.fill(0)
        display.text(device_name, text_x_center_position(device_name), 20, 255)
        display_menu(STeaMi_founded, STeaMi_index)
        display.show()
        await asyncio.sleep(0.1)  # if don't sleep, the scan task will not work

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

async def scan_task():
    while True:
        print("---Starting Scan---")
        STeaMi_founded.clear()
        async with aioble.scan(500, interval_us=30000, window_us=30000, active=True) as scanner:
            async for result in scanner:
                name = result.name()
                if name and name.startswith("STeaMi"):
                    print(f"=> Found sensor : {name}")
                    if name not in STeaMi_founded:
                        STeaMi_founded.append(name)
        await asyncio.sleep(1)

# asyncio.run(scan_task())

# Runs the main tasks concurrently
async def main():
    t1 = asyncio.create_task(scan_task())
    t3 = asyncio.create_task(display_task())
    t4 = asyncio.create_task(button_task())
    await asyncio.gather(t1, t3,t4)

asyncio.run(main())