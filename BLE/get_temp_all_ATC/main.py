import aioble
import asyncio
import bluetooth
import struct

# Adresse MAC à filtrer
MAC_ADDRESS_FILTER = "A4:C1:38"

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)

# Fonction pour générer le nom basé sur la MAC
def generate_name_from_mac(addr):
    mac_address = ':'.join(['%02x' % b for b in addr]).upper()
    mac_suffix = mac_address.replace(":", "")[-6:]  # Récupère les 6 derniers caractères de la MAC
    return f"ATC_{mac_suffix}"

def _decode_temperature(data):
    return struct.unpack("<h", data)[0] / 100

async def find_sensors():
    matching_devices = []
    print(f"--- Scanning with '{MAC_ADDRESS_FILTER}' ---")

    async with aioble.scan(5000, interval_us=30000, window_us=30000) as scanner:
        async for result in scanner:
            mac_address = ':'.join(['%02x' % b for b in result.device.addr]).upper()
            if mac_address.startswith(MAC_ADDRESS_FILTER):  # Filtrage des adresses MAC
                print(f"==> Found sensor name : {result.name() or generate_name_from_mac(result.device.addr)}")
                matching_devices.append(result.device)
    
    if not matching_devices:
        print(f"/!\ No devices found matching the MAC prefix '{MAC_ADDRESS_FILTER}'")
    return matching_devices

async def connect_to_device(device):
    print(f"-> connect to : {generate_name_from_mac(device.addr)}")
    try:
        await asyncio.sleep(2)  # Add a small delay before attempting the connection
        connection = await device.connect()
        print(f"--> connected to {generate_name_from_mac(device.addr)}")
        return connection
    except Exception as e:
        print(f"/!\ Error connecting to device {generate_name_from_mac(device.addr)}: {e}")
        print(f"/!\ Error details: {e.args}")
        return None

async def main():
    print("---Starting Scan---")
    devices = await find_sensors()
    
    if not devices:
        print("/!\ No matching devices found. Exiting scan.")
        return

    # Tentative de connexion à chaque appareil trouvé
    for device in devices:
        print(f"> TRY connect {generate_name_from_mac(device.addr)}---")
        connection = await connect_to_device(device)
        
        if connection is None:
            print(f"/!\ Connection failed to device {generate_name_from_mac(device.addr)}. Skipping to next.")
            continue  # Passer à l'appareil suivant si la connexion échoue
        
        async with connection:
            try:
                temp_service = await connection.service(_ENV_SENSE_UUID)
                if temp_service is None:
                    print(f"/!\ Service {_ENV_SENSE_UUID} non trouvé pour {generate_name_from_mac(device.addr)}.")
                    continue
                temp_characteristic = await temp_service.characteristic(_ENV_SENSE_TEMP_UUID)
                if temp_characteristic is None:
                    print(f"/!\ Caractéristique {_ENV_SENSE_TEMP_UUID} non trouvée pour {generate_name_from_mac(device.addr)}.")
                    continue
                print(f"---> Found service : {generate_name_from_mac(device.addr)}")
            except asyncio.TimeoutError:
                print(f"/!\ Timeout while discovering services/characteristics for device {generate_name_from_mac(device.addr)}. Skipping.")
                continue  # Passer à l'appareil suivant en cas de timeout
            
            # Lecture des données de température tant que l'appareil est connecté
            while connection.is_connected():
                try:
                    temp_deg_c = _decode_temperature(await temp_characteristic.read(timeout_ms=3000))
                    print(f"{generate_name_from_mac(device.addr)} : {temp_deg_c:.2f} °C")
                except asyncio.TimeoutError:
                    print(f"/!\ Timeout reading temperature from device {device.addr}. Trying again.")
                await asyncio.sleep_ms(1000)

    print("---Scan finished---")

# Lancer le scan
asyncio.run(main())