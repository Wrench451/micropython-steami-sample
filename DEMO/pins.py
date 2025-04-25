from pyb import Pin
import asyncio
from time import sleep

LED_RED = Pin("LED_RED", Pin.OUT_PP)
LED_GREEN = Pin("LED_GREEN", Pin.OUT_PP)
LED_BLUE = Pin("LED_BLUE", Pin.OUT_PP)

A_BUTTON = Pin("A_BUTTON", Pin.IN, Pin.PULL_UP)
B_BUTTON = Pin("B_BUTTON", Pin.IN, Pin.PULL_UP)
MENU_BUTTON = Pin("MENU_BUTTON", Pin.IN, Pin.PULL_UP)

SPEAKER = Pin("SPEAKER", Pin.OUT_PP)

INT_DIST = Pin("INT_DIST")

async def wait_for_button():
    while True:
        if A_BUTTON.value() == 0:
            sleep(0.2)
            return "A"
        elif B_BUTTON.value() == 0:
            sleep(0.2)
            return "B"
        elif MENU_BUTTON.value() == 0:
            sleep(0.2)
            return "MENU"
        await asyncio.sleep(0.1)