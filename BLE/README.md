## 🛠 BLE Timeout Issue on NUCLEO-WB55

If you encounter a **timeout or failure** when calling:

```python
from bluetooth import BLE
BLE().active(True)
```

This may be due to a missing or incompatible BLE firmware on your STM32WB chip.

### ✅ Solution:

Flash the following firmware:
[`stm32wb5x_BLE_HCILayer_extended_fw.bin` (v1.21.0)](https://github.com/STMicroelectronics/STM32CubeWB/blob/v1.21.0/Projects/STM32WB_Copro_Wireless_Binaries/STM32WB5x/stm32wb5x_BLE_HCILayer_extended_fw.bin)

- Load address: `0x080DA000` *(for STM32WB5xxG with 1MB Flash)*
- Once flashed, BLE should activate without issues:

```python
>>> from bluetooth import BLE
>>> BLE().active(True)
True
```

This fixes the BLE activation timeout on the NUCLEO_WB55 board.