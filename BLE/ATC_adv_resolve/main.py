import aioble
import asyncio
import bluetooth
import struct

MAC_ADDRESS_FILTER = "A4:C1:38" #:3F:19:D6"

collected_data = []

# def _decode_data(data):
#     return struct.unpack("<h", data)[0] / 100

def _decode_humidity(data):
    data = data[3:5]
    return struct.unpack("<h", data)[0] / 100

def _decode_temperature(data):
    data = data[13:15]
    return struct.unpack("<h", data)[0] / 100

def generate_name_from_mac(addr):
    mac_address = ':'.join(['%02x' % b for b in addr]).upper()
    mac_suffix = mac_address.replace(":", "")[-6:] 
    return f"ATC_{mac_suffix}"

async def main():
    print(f"---Starting Scan With Filter {MAC_ADDRESS_FILTER}---")
    for scan_round in range(5):
        async with aioble.scan(1000, interval_us=30000, window_us=30000) as scanner:
            async for result in scanner:
                mac_address = ':'.join(['%02x' % b for b in result.device.addr]).upper()
                if mac_address.startswith(MAC_ADDRESS_FILTER):  
                    print(f"==> Found sensor name : {result.name() or generate_name_from_mac(result.device.addr)}")
                    if (len(result.adv_data) <= 17):
                        print(f"Invalid data length: {len(result.adv_data)}")
                        continue
                    print(f"Temperature : {_decode_temperature(result.adv_data)}")
                    print(f"Humidity : {_decode_humidity(result.adv_data)}")
                    collected_data.append({
                            "sensor": generate_name_from_mac(result.device.addr),
                            "temperature": _decode_temperature(result.adv_data),
                            "humidity": _decode_humidity(result.adv_data),
                            "scan_round": scan_round
                        })


asyncio.run(main())
print("\n--- Récapitulatif des données collectées ---")
for data in collected_data:
    print(f"Capteur: {data['sensor']}, Température: {data['temperature']:.2f} °C, Humidité : {data['humidity']:.2f}, Scan Round: {data['scan_round']}")