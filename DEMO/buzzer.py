from pins import *
from time import sleep

sounds = ["HIGH", "DOWN", "MID","EXIT"]

def play_sound(sound_index):
    if sound_index == 0:
        SPEAKER.duty(512)
        SPEAKER.freq(2000)
    elif sound_index == 1:
        SPEAKER.duty(512)
        SPEAKER.freq(1000)
    elif sound_index == 2:
        SPEAKER.duty(512)
        SPEAKER.freq(1500)

async def buzzer_menu():
    print("--- BUZZER ---")
    print("A/B : naviguate | Menu : select")

    sounds_index = 0
    display_menu("BUZZER", sounds, sounds_index)
    while True:
        print(f"> {sounds[sounds_index]}")
        btn = await wait_for_button()

        if btn == "A":
            sounds_index -= 1
        elif btn == "B":
            sounds_index += 1
        elif btn == "MENU":
            if sounds[sounds_index] == "EXIT":
                break
            play_sound(sounds_index)
            break

        if sounds_index >= len(sounds) : sounds_index = 0
        elif sounds_index < 0 : sounds_index = len(sounds) - 1
        display_menu("BUZZER", sounds, sounds_index)