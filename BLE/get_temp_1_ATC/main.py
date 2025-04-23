import aioble
import asyncio
import bluetooth
import random
import struct

# Adresse MAC à filtrer
MAC_ADDRESS_FILTER = "A4:C1:38:3F:19:D6"

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)

# Fonction pour générer le nom basé sur la MAC
def generate_name_from_mac(mac_address):
    mac_suffix = mac_address.replace(":", "")[-6:]  # Récupère les 6 derniers caractères de la MAC
    return f"ATC_{mac_suffix}"

def _decode_temperature(data):
    return struct.unpack("<h", data)[0] / 100

async def find_sensor():
    async with aioble.scan(5000, interval_us=30000, window_us=30000) as scanner:
        async for result in scanner:
            mac_address = ':'.join(['%02x' % b for b in result.device.addr]).upper()
            if mac_address == MAC_ADDRESS_FILTER:
                print(f"MAC: {mac_address}")
                print(f"RSSI : {result.rssi}")
                print(f"Payload brut : {result.adv_data}")
                print(f"Nom du capteur : {result.name() or generate_name_from_mac(mac_address)}")
                
                return result.device
    return None

async def main():
    print("---Start Scan---")
    device = await find_sensor()
    
    if device is None:
        print("/!\ sensor not found")
        return

    try:
        print("-> Connecting to", device.addr)
        await asyncio.sleep(2)
        connection = await device.connect()
        print(f"-> Connected to {device}")
    except Exception as e:
        print(f"/!\ Error connecting: {e}")
        print(f"/!\ Detail :{e.args}")
        return
    
    async with connection:
        try:
            temp_service = await connection.service(_ENV_SENSE_UUID)
            temp_characteristic = await temp_service.characteristic(_ENV_SENSE_TEMP_UUID)
            print("-> Service and Characteristic founded")
        except asyncio.TimeoutError:
            print("/!\ Timeout discovering services/characteristics")
            return
        
        while connection.is_connected():
            temp_deg_c = _decode_temperature(await temp_characteristic.read(timeout_ms=3000))
            print("Temperature: {:.2f}".format(temp_deg_c))
            await asyncio.sleep_ms(1000)
    print("---sortie de scan---")
# Lancer le scan
asyncio.run(main())