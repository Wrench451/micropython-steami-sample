import aioble
import asyncio
import struct
from pyb import Pin
from time import sleep

MAC_ADDRESS_FILTER = "A4:C1:38"
ROUNDS = 1
SCAN_DURATION = 5000

LED_RED = Pin("LED_RED", Pin.OUT_PP)
LED_GREEN = Pin("LED_GREEN", Pin.OUT_PP)
BTN_A = Pin("A_BUTTON", Pin.IN, Pin.PULL_UP)
BTN_B = Pin("B_BUTTON", Pin.IN, Pin.PULL_UP)

devices = []
collected_data = []

def _decode_humidity(data):
    data = data[3:5]
    return struct.unpack("<h", data)[0] / 100

def _decode_temperature(data):
    data = data[13:15]
    return struct.unpack("<h", data)[0] / 100

def _decode_name(addr):
    mac_address = ':'.join(['%02x' % b for b in addr]).upper()
    mac_suffix = mac_address.replace(":", "")[-6:] 
    return f"ATC_{mac_suffix}"

async def scan_temp():
    print(f"---Starting Scan With Filter {MAC_ADDRESS_FILTER}---")
    for scan_round in range(ROUNDS):
        async with aioble.scan(SCAN_DURATION, interval_us=30000, window_us=30000) as scanner:
            async for result in scanner:
                if result.device.addr in devices:  
                    print(f"==> Found sensor name : {result.name() or _decode_name(result.device.addr)}")
                    if (len(result.adv_data) <= 17): # 17 bytes is the minimum length for valid data
                        print(f"Invalid data length: {len(result.adv_data)}")
                        continue
                    print(f"Temperature : {_decode_temperature(result.adv_data)}")
                    print(f"Humidity : {_decode_humidity(result.adv_data)}")
                    collected_data.append({
                            "sensor": _decode_name(result.device.addr),
                            "temperature": _decode_temperature(result.adv_data),
                            "humidity": _decode_humidity(result.adv_data),
                            "scan_round": scan_round
                        })

async def scan_ble():
    print("--- Scanning for BLE devices... ---")
    async with aioble.scan(500, interval_us=30000, window_us=30000) as scanner:
        async for result in scanner:
            mac_address = ':'.join(['%02x' % b for b in result.device.addr]).upper()
            if mac_address.startswith(MAC_ADDRESS_FILTER):
                print(f"Found device: {mac_address}, Name: {result.name() or _decode_name(result.device.addr)}")
                devices.append(result.device.addr)

async def wait_for_button_press():
    while True:
        if BTN_A.value() == 0:
            return ("A")
        elif BTN_B.value() == 0:
            return ("B")
        await asyncio.sleep(0.1)

async def select_device():
    print("Select a device to connect to (A : yes / B : no ):")
    selected_devices = []
    for i, device in enumerate(devices[:]):
        print(f"{i + 1}: {_decode_name(device)}")
        btn = await wait_for_button_press()
        if btn == "A":
            print("Selected")
            LED_GREEN.on()
            sleep(0.5)
            LED_GREEN.off()
            selected_devices.append(device)
        elif btn == "B":
            print("Not selected")
            LED_RED.on()
            sleep(0.5)
            LED_RED.off()
        else:
            print("Invalid selection")
            continue
        sleep(0.5)
    devices[:] = selected_devices


asyncio.run(scan_ble())
asyncio.run(select_device())

asyncio.run(scan_temp())
print("\n--- Récapitulatif des données collectées ---")
for data in collected_data:
    print(f"Capteur: {data['sensor']}, Température: {data['temperature']:.2f} °C, Humidité : {data['humidity']:.2f}, Scan Round: {data['scan_round']}")