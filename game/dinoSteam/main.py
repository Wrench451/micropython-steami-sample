import asyncio
import framebuf
from pins import *

# Bitmaps
STeaMi_bitmap = bytearray([
    0b00111100,
    0b01111110,
    0b11111111,
    0b11011101,
    0b10101010,
    0b11111111,
    0b11111111,
    0b01111110,
    0b00111100,
    0b01111110,
    0b11111111,
])

Cactus_bitmap = bytearray([
    0b00100000,
    0b00101000,
    0b10111000,
    0b11100000,
    0b00100000,
    0b00100000,
])

# Framebuffers
STeaMi_buf = framebuf.FrameBuffer(STeaMi_bitmap, 8, 11, framebuf.MONO_HLSB)
Cactus_buf = framebuf.FrameBuffer(Cactus_bitmap, 8, 6, framebuf.MONO_HLSB)

# Boutons
A_BUTTON = Pin("A_BUTTON", Pin.IN, Pin.PULL_UP)
B_BUTTON = Pin("B_BUTTON", Pin.IN, Pin.PULL_UP)
MENU_BUTTON = Pin("MENU_BUTTON", Pin.IN, Pin.PULL_UP)

# Constantes
GRAVITY = 0.5
JUMP_SMALL = -5
JUMP_BIG = -6
GROUND_Y = 78
STeaMi_X = 20

# Fonctions
def draw_background():
    display.fill(0)
    display.framebuf.line(0, 90, 128, 90, 255)

def draw_STeaMi(x, y):
    display.framebuf.blit(STeaMi_buf, x, y)

def draw_Cactus(x):
    display.framebuf.blit(Cactus_buf, x, 90 - 6)

def clean_score_zone():
    display.framebuf.fill_rect(60, 100, 30, 10, 0)

async def wait_for_button(button):
    while button.value() != 0:
        await asyncio.sleep(0.02)

async def menu_screen():
    display.fill(0)
    display.framebuf.text("Dino Steam", 25, 40, 255)
    display.framebuf.text("Menu to start", 10, 70, 50)
    display.framebuf.text("A/B to jump", 18, 80, 50)
    display.show()
    await wait_for_button(MENU_BUTTON)
    await asyncio.sleep(0.2)  # Anti double appui

async def game_screen():
    pos_cactus = 120
    y_steami = GROUND_Y
    y_velocity = 0
    points = 0

    while True:
        display.fill(0)
        draw_background()

        # Déplacement cactus
        pos_cactus -= 1
        if pos_cactus < -10:
            pos_cactus = 128
            points += 1

        draw_Cactus(pos_cactus)

        # Gestion saut
        if A_BUTTON.value() == 0 and y_steami == GROUND_Y:
            y_velocity = JUMP_SMALL
        if B_BUTTON.value() == 0 and y_steami == GROUND_Y:
            y_velocity = JUMP_BIG
        

        # Gravité
        y_steami += y_velocity
        y_velocity += GRAVITY

        if y_steami > GROUND_Y:
            y_steami = GROUND_Y
            y_velocity = 0

        draw_STeaMi(STeaMi_X, int(y_steami))

        # Afficher le score
        display.framebuf.text("{}".format(points), 64, 100, 255)

        # Collision simple
        if (STeaMi_X + 8 > pos_cactus and STeaMi_X < pos_cactus + 5) and (y_steami > 70):
            return points  # Meurt => retourne le score

        # Faire une pause
        if MENU_BUTTON.value() == 0:
            while MENU_BUTTON.value() == 0:
                await asyncio.sleep(0.02)
            # Puis attendre un 2e appui pour continuer
            display.framebuf.text("Pause", 40, 40, 255)
            display.show()
            while MENU_BUTTON.value() == 1:
                await asyncio.sleep(0.02)
            while MENU_BUTTON.value() == 0:
                await asyncio.sleep(0.02)

        display.show()
        await asyncio.sleep(0.02)

async def game_over_screen(points):
    display.fill(0)
    display.framebuf.text("GAME OVER!", 25, 40, 255)
    display.framebuf.text("Score: {}".format(points), 30, 60, 255)
    display.framebuf.text("Menu to restart", 5, 80, 50)
    display.show()
    await wait_for_button(MENU_BUTTON)
    await asyncio.sleep(0.2)  # Anti double appui

async def main():
    await menu_screen()
    while True:
        score = await game_screen()
        await game_over_screen(score)

# Lancer le jeu
asyncio.run(main())
