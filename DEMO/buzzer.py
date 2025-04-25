from pins import *
from time import sleep

sounds = ["HIGH", "DOWN", "MID"]

async def buzzer_menu():
    print("--- BUZZER ---")
    print("A/B : naviguate | Menu : select")

    sounds_index = 0

    while True:
        print(f"> {sounds[sounds_index]}")
        btn = await wait_for_button()

        if btn == "A":
            sounds_index += 1
        elif btn == "B":
            sounds_index -= 1
        elif btn == "MENU":
            break

        if sounds_index >= len(sounds) : sounds_index = 0
        elif sounds_index < 0 : sounds_index = len(sounds) - 1