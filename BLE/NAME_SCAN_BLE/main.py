import bluetooth
import time
from micropython import const
from ble_advertising import decode_services, decode_name

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)

_UUID_NAMES = {
    bluetooth.UUID(0x2A00): "Device Name",
    bluetooth.UUID(0x2A01): "Appearance",
    bluetooth.UUID(0x2A04): "Preferred Connection Parameters",
    bluetooth.UUID(0x2AC9): "Local Name",
}

class BLESimpleCentral:
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._reset()

    def _reset(self):
        self._found_devices = []
        self._seen_addrs = set()
        self._conn_handle = None
        self._services = []
        self._characteristics = []
        self._current_device = None
        self._char_index = 0
        self._connect_start = None

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            if adv_type in (_ADV_IND, _ADV_DIRECT_IND):
                addr = bytes(addr)
                if (addr_type, addr) not in self._seen_addrs:
                    name = decode_name(adv_data) or "?"
                    services = decode_services(adv_data)
                    print(f"[SCAN] Found device: {addr_type} {addr} | RSSI: {rssi} | Name: {name} | Services: {services}")
                    self._seen_addrs.add((addr_type, addr))
                    self._found_devices.append((addr_type, addr, name))

        elif event == _IRQ_SCAN_DONE:
            print("\n[INFO] Scan complete. Devices found:")
            for addr_type, addr, name in self._found_devices:
                print(f"  - {addr_type} {addr} → {name}")
            if self._found_devices:
                self._connect_next()
            else:
                print("[INFO] No peripherals found.")

        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            if self._current_device and addr_type == self._current_device[0] and addr == self._current_device[1]:
                self._conn_handle = conn_handle
                self._services = []
                self._characteristics = []
                self._ble.gattc_discover_services(conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                print(f"[INFO] Disconnected from {self._current_device[1]}\n")
                self._conn_handle = None
                self._connect_next()

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start_handle, end_handle, uuid = data
            if conn_handle == self._conn_handle:
                self._services.append((start_handle, end_handle, uuid))

        elif event == _IRQ_GATTC_SERVICE_DONE:
            if self._services:
                start, end, _ = self._services[0]  # Explore first service only for now
                self._ble.gattc_discover_characteristics(self._conn_handle, start, end)
            else:
                self._ble.gap_disconnect(self._conn_handle)

        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self._conn_handle:
                self._characteristics.append((value_handle, uuid))

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            if self._characteristics:
                self._char_index = 0
                self._read_next_characteristic()
            else:
                print("[WARN] No characteristics found.")
                self._ble.gap_disconnect(self._conn_handle)

        elif event == _IRQ_GATTC_READ_RESULT:
            conn_handle, value_handle, char_data = data
            try:
                decoded = bytes(char_data).decode().strip()
                print(f"[CHAR] Handle: {value_handle} → \"{decoded}\"")
            except:
                print(f"[CHAR] Handle: {value_handle} → {char_data}")

        elif event == _IRQ_GATTC_READ_DONE:
            self._char_index += 1
            self._read_next_characteristic()

    def _read_next_characteristic(self):
        if self._char_index < len(self._characteristics):
            handle, uuid = self._characteristics[self._char_index]
            uuid_name = _UUID_NAMES.get(uuid, str(uuid))
            print(f"[READ] Characteristic {self._char_index + 1}/{len(self._characteristics)} | UUID: {uuid_name}")
            self._ble.gattc_read(self._conn_handle, handle)
        else:
            self._ble.gap_disconnect(self._conn_handle)

    def _connect_next(self):
        if not self._found_devices:
            print("[DONE] All devices tested.")
            return
        self._services = []
        self._characteristics = []
        self._conn_handle = None
        self._current_device = self._found_devices.pop(0)
        addr_type, addr, name = self._current_device
        print(f"\n[CONNECT] Connecting to {addr_type} {addr} ({name})...")
        self._connect_start = time.ticks_ms()
        self._ble.gap_connect(addr_type, addr)

    def scan(self):
        self._reset()
        self._ble.gap_scan(10000, 30000, 30000, True)


def demo():
    ble = bluetooth.BLE()
    central = BLESimpleCentral(ble)
    central.scan()

    while True:
        if central._current_device and central._conn_handle is None and central._connect_start:
            if time.ticks_diff(time.ticks_ms(), central._connect_start) > 5000:
                print("[TIMEOUT] Connection timeout, skipping...\n")
                try:
                    central._ble.gap_disconnect(0)
                except:
                    pass
                central._connect_start = None
                central._connect_next()
        time.sleep_ms(100)

if __name__ == "__main__":
    demo()