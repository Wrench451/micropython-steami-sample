from pins import *
from time import sleep
import math

sounds = ["HAPPY", "SAD", "EPIC","EXIT"]

def draw_progress_arc(display, center_x, center_y, radius, percent):
    angle = int(360 * percent)
    for a in range(angle):
        rad = math.radians(a)
        for r in [radius, radius - 1]:  # deux cercles concentriques
            x = int(center_x + r * math.cos(rad))
            y = int(center_y + r * math.sin(rad))
            display.pixel(x, y, 255)

def tone(pin, freq, duration_ms):
    if freq == 0:
        time.sleep_ms(duration_ms)
        return
    period_us = int(1_000_000 / freq)
    half_period = period_us // 2
    end_time = time.ticks_add(time.ticks_us(), duration_ms * 1000)
    while time.ticks_diff(end_time, time.ticks_us()) > 0:
        pin.on()
        time.sleep_us(half_period)
        pin.off()
        time.sleep_us(half_period)

def play_song(song):
    start = time.ticks_ms()
    duration_total = sum(duration for _, duration in song)
    center = 64
    radius = 62

    for freq, duration in song:
        tone(SPEAKER, freq, duration)
        time.sleep_ms(30)

        # Calcul du pourcentage de progression
        elapsed = time.ticks_diff(time.ticks_ms(), start)
        percent = min(elapsed / duration_total, 1.0)

        # Dessine la progression circulaire
        draw_progress_arc(display, center, center, radius, percent)
        display.show()

        if elapsed >= duration_total:
            break

def play_sound(sound_index):
    if sound_index == 0:
        joyful_song = [
                (523, 200), (659, 200), (784, 300), (659, 200),
                (784, 200), (880, 300), (0, 100),
                (784, 150), (880, 150), (988, 400), (0, 100),
                (880, 200), (784, 200), (659, 300)
            ]
        play_song(joyful_song)
    elif sound_index == 1:
        sad_song = [
            (659, 400), (0, 100), (587, 300), (0, 100),
            (523, 500), (0, 100), (494, 400),
            (523, 600), (0, 200), (440, 300),
            (392, 600), (0, 200), (440, 300)
        ]
        play_song(sad_song)
    elif sound_index == 2:
        epic_song = [
            (440, 100), (523, 100), (659, 200), (784, 200), (988, 300),
            (880, 100), (784, 100), (659, 200), (0, 100),
            (659, 100), (784, 100), (988, 300),
            (1047, 400), (988, 150), (880, 150), (784, 300)
        ]
        play_song(epic_song)


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

        if sounds_index >= len(sounds) : sounds_index = 0
        elif sounds_index < 0 : sounds_index = len(sounds) - 1
        display_menu("BUZZER", sounds, sounds_index)