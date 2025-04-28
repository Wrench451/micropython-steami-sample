import aioble

from pins import *

ble = ["RECEIVE", "EMIT"]

async def ble_menu():
    print("--- BLE ---")
    print("A to RECEIVE | B to EMIT | MENU to EXIT")

    while True:
        btn = await wait_for_button()
        if btn == "A":
            print("BLE RECEIVE")
            await ble_receive()
        elif btn == "B":
            print("BLE EMIT")
            await ble_emit()
        elif btn == "MENU":
            break
        print("A to RECEIVE | B to EMIT | MENU to EXIT")

async def ble_receive():
    async with aioble.scan(500, interval_us=30000, window_us=30000) as scanner:
        async for result in scanner:
            mac_address = ':'.join(['%02x' % b for b in result.device.addr]).upper()  
            print(f"MAC: {mac_address}")
            print(f"RSSI : {result.rssi}")
            print(f"Payload brut : {result.adv_data}")
            print(f"Nom du capteur : {result.name() or 'none'}")
            return
        
async def ble_emit():
    print("BLE EMIT")
    print("A to SEND | MENU to EXIT")
    iteration = 0
    while True:
        btn = await wait_for_button()
        if btn == "A":
            async with await aioble.advertise(
                3000,
                name="STeaMi",
                payload=b"Hello World",
                interval_us=30000,
                timeout_ms=5000) as adv:

                print("Advertising...")
                await adv.advertise()
                print("Advertising done")
                iteration += 1
        elif btn == "MENU":
            break
        print("A to SEND | MENU to EXIT")