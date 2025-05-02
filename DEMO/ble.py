import aioble

from pins import *

ble = ["RECEIVE", "EMIT", "EXIT"]

async def run_ble(ble_index):
    if ble_index == 0:
        print("BLE RECEIVE")
        display.fill(0)
        display.text("BLE SCAN ... ", 25, 70, 255)
        display.show()
        results = await ble_receive()
        await display_receive(results)
    elif ble_index == 1:
        print("BLE EMIT")
        ble_emit()
    elif ble_index == 2:    
        return

async def ble_menu():
    print("--- BLE ---")

    ble_index = 0
    display_menu("BLE", ble, ble_index)

    while True:
        btn = await wait_for_button()
        if btn == "A":
            ble_index -= 1
        elif btn == "B":
            ble_index += 1
        elif btn == "MENU":
            if ble[ble_index] == "EXIT":
                break
            await run_ble(ble_index)
        if ble_index >= len(ble) : ble_index = 0
        elif ble_index < 0 : ble_index = len(ble) - 1
        display_menu("BLE", ble, ble_index)

async def ble_receive():
    print("START BLE SCAN")
    results = []
    async with aioble.scan(1000, interval_us=30000, window_us=30000) as scanner:
        async for result in scanner:
            results.append(result)
    
    return results
    print("END BLE SCAN")
    

async def display_receive(results):
    print("BLE SCAN RESULTS")
    
    result_index = 0
    while True:
        print(f"{result_index+1}/{len(results)}: {results[result_index]}")

        display.fill(0)
        display.text("RESULTS", 35, 20, 255)
        if not results:
            print("Aucun résultat à afficher.")
            display.text("No results to show", 20, 50, 255)
            return
        else :
            display.text(f"{result_index+1}/{len(results)}", 50, 30, 255)
            mac_address = ''.join(['%02x' % b for b in results[result_index].device.addr]).upper()
            display.text("MAC address:", 20, 50, 255)
            display.text(f"{mac_address}", 15, 60, 255)
            display.text(f"RSSI : {results[result_index].rssi}", 20, 80, 255)
            display.text(f"Name : {results[result_index].name()}", 20, 100, 255)
       
        display.show()

        btn = await wait_for_button()
        if btn == "A":
            result_index -= 1
        elif btn == "B":
            result_index += 1
        elif btn == "MENU":
            break
        if result_index >= len(results) : result_index = 0
        elif result_index < 0 : result_index = len(results) - 1


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