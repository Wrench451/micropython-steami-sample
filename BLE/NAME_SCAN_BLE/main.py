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

_DEVICE_NAME_UUID = bluetooth.UUID(0x2A00)
_GENERIC_ACCESS_UUID = bluetooth.UUID(0x1800)


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
        self._ga_start = None
        self._ga_end = None
        self._name_handle = None
        self._current_device = None
        self._read_callback = None
        self._connect_start = None

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            if adv_type in (_ADV_IND, _ADV_DIRECT_IND):
                addr = bytes(addr)
                if (addr_type, addr) not in self._seen_addrs:
                    name = decode_name(adv_data) or "?"
                    self._seen_addrs.add((addr_type, addr))
                    self._found_devices.append((addr_type, addr, name))

        elif event == _IRQ_SCAN_DONE:
            print("Scan complete. Found devices:")
            for addr_type, addr, name in self._found_devices:
                print("-", addr_type, addr, name)
            if self._found_devices:
                self._connect_next()
            else:
                print("No peripherals found.")

        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            if self._current_device and addr_type == self._current_device[0] and addr == self._current_device[1]:
                self._conn_handle = conn_handle
                self._ble.gattc_discover_services(conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                print(f"Disconnected from {self._current_device[1]}")
                self._conn_handle = None
                self._connect_next()

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start_handle, end_handle, uuid = data
            if conn_handle == self._conn_handle and uuid == _GENERIC_ACCESS_UUID:
                self._ga_start = start_handle
                self._ga_end = end_handle

        elif event == _IRQ_GATTC_SERVICE_DONE:
            if self._ga_start and self._ga_end:
                self._ble.gattc_discover_characteristics(self._conn_handle, self._ga_start, self._ga_end)
            else:
                self._ble.gap_disconnect(self._conn_handle)

        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self._conn_handle and uuid == _DEVICE_NAME_UUID:
                self._name_handle = value_handle

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            if self._name_handle:
                self.read_name(self._read_callback)
            else:
                print(f"[GATT] {self._current_device[1]}: No name characteristic found.")
                self._ble.gap_disconnect(self._conn_handle)

        elif event == _IRQ_GATTC_READ_RESULT:
            conn_handle, value_handle, char_data = data
            if self._read_callback:
                self._read_callback(self._current_device, char_data)

        elif event == _IRQ_GATTC_READ_DONE:
            conn_handle, value_handle, status = data
            self._ble.gap_disconnect(conn_handle)

    def _connect_next(self):
        if not self._found_devices:
            print("All devices tested.")
            return
        self._ga_start = None
        self._ga_end = None
        self._name_handle = None
        self._conn_handle = None
        self._current_device = self._found_devices.pop(0)
        addr_type, addr, name = self._current_device
        print(f"Connecting to {addr_type} {addr} ({name})...")
        self._connect_start = time.ticks_ms()
        self._ble.gap_connect(addr_type, addr)

    def scan(self):
        self._reset()
        self._ble.gap_scan(10000, 30000, 30000, True)

    def read_name(self, callback):
        self._read_callback = callback
        if self._name_handle:
            self._ble.gattc_read(self._conn_handle, self._name_handle)
        else:
            # fallback: print the name from advertisement
            if self._current_device:
                addr_type, addr, adv_name = self._current_device
                print(f"[ADV] {addr_type} {addr}: {adv_name}")
            self._ble.gap_disconnect(self._conn_handle)


def demo():
    ble = bluetooth.BLE()
    central = BLESimpleCentral(ble)

    def on_name_read(device, name_bytes):
        addr_type, addr, adv_name = device
        try:
            name = name_bytes.decode()
            print(f"[GATT] {addr_type} {addr}: {name}")
        except:
            print(f"[GATT] {addr_type} {addr}: Failed to decode name")

    central._read_callback = on_name_read
    central.scan()

    while True:
        if central._current_device and central._conn_handle is None and central._connect_start:
            if time.ticks_diff(time.ticks_ms(), central._connect_start) > 5000:
                print("Connection timeout, skipping...")
                try:
                    central._ble.gap_disconnect(0)
                except:
                    pass
                central._connect_start = None
                central._connect_next()
        time.sleep_ms(100)

if __name__ == "__main__":
    demo()