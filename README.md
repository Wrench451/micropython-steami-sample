Parfait ! Voici une version du `README.md` mise à jour pour utiliser **`mpremote`**, qui est l’outil recommandé par MicroPython pour interagir avec les microcontrôleurs.

---

# MicroPython STEAMI Sample

A collection of MicroPython sample scripts for the **STM32WB55** microcontroller. These examples demonstrate a wide range of features such as LED control, button input, BLE communication, sensor reading, display management, and simple games — ideal for STEAM education and embedded experimentation.

---

## 📁 Project Structure

```
micropython-steami-sample/
│
├── BLE/        # Bluetooth Low Energy communication
├── BUTTON/     # Button input examples
├── DEMO/       # Combined demos (e.g., sensors + screen)
├── GAME/       # Mini games in MicroPython
├── LED/        # LED control and animations
├── SCREEN/     # Display output examples (e.g., OLED)
├── SENSOR/     # Sensor data acquisition
```

Each folder contains example `.py` scripts you can run directly on your STM32WB55 board.

---

## ✅ Requirements

* **Hardware**: STM32WB55 development board
* **Firmware**: MicroPython for STM32WB55 (flashed)
* **Tooling**:

  * [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) (official MicroPython tool)

---

## 🚀 Quick Start with `mpremote`

1. **Install mpremote** if not already installed:

   ```bash
   pip install mpremote
   ```

2. **Connect your board** via USB and verify it's detected:

   ```bash
   mpremote connect list
   ```

3. **Upload and run a script**:

   For example, to run the LED blink demo:

   ```bash
   mpremote connect auto fs cp LED/blink.py :main.py
   mpremote connect auto reset
   ```

   This copies the script to your board and sets it to run on boot.

4. **Open a REPL (optional)**:

   ```bash
   mpremote connect auto
   ```

   Then press `Ctrl+C` to stop current execution or `Ctrl+D` to soft reset.

---

## 🧪 Examples

* `LED/blink.py` — basic LED blink
* `BUTTON/read_button.py` — detect button press
* `BLE/advertiser.py` — advertise as BLE device
* `SCREEN/oled_demo.py` — print to OLED screen
* `GAME/dinoSteam.py` — a simple built-in game

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributions

Feel free to contribute by submitting pull requests, improving examples, or reporting issues!

---

Let me know if you'd like a `requirements.txt`, setup guide for firmware flashing, or a README translation!
