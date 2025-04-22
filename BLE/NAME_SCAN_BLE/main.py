import aioble
import asyncio

# Adresse MAC à filtrer
MAC_ADDRESS_FILTER = "A4:C1:38:3F:19:D6"

# Fonction pour générer le nom basé sur la MAC
def generate_name_from_mac(mac_address):
    mac_suffix = mac_address.replace(":", "")[-6:]  # Récupère les 6 derniers caractères de la MAC
    return f"ATC_{mac_suffix}"

# Fonction pour scanner les appareils BLE avec un filtre sur l'adresse MAC
async def filtered_scan():
    print(f"Scanning for devices with MAC address: {MAC_ADDRESS_FILTER}...\n \n")
    async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000) as scanner:
        async for result in scanner:
            mac_address = ':'.join(['%02x' % b for b in result.device.addr]).upper()
            if mac_address == MAC_ADDRESS_FILTER:
                print(f"MAC: {mac_address} RSSI: {result.rssi}")
                print(f"Payload brut : {result.adv_data}")

                # Afficher le nom du dispositif ou générer un nom basé sur l'adresse MAC
                nom_capteur = result.name() or generate_name_from_mac(mac_address)
                print(f"Nom du capteur : {nom_capteur}")
    print("\n \n Scan terminé.")

# Lancer le scan
asyncio.run(filtered_scan())
