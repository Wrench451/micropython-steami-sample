from pins import *
from time import sleep

async def button_menu():
    print("--- BUTTON ---")

    while True:
        joystick_move = await wait_for_button()
        if joystick_move == "A":
            print("A button pressed")
        elif joystick_move == "B":
            print("B button pressed")
        elif joystick_move == "MENU":
            print("Menu button pressed")
            break