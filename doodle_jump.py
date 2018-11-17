# Written by Simeng Hao (sh4aj) and Derek Habron (hjb5ek)
from random import randint

import pygame

import gamebox

# Key attributes
PLATFORM_HEIGHT = 10
PLATFORM_WIDTH = 60
VERTICAL_DIST_BTW_PLATFORMS = 100
PLATFORM_COUNT = 6
PLAYER_X_SPEED_INCREMENT = 5
FRICTION = 0.7
CAMERA_WIDTH = 400
CAMERA_HEIGHT = 600


# Definitions:
def rand_platform_x():
    return randint(PLATFORM_WIDTH / 2, CAMERA_WIDTH - (PLATFORM_WIDTH / 2) + 1)


def respawn(box, x, y):
    # assert type(box) == type(gamebox.from_color(0,0,"0x000000",0,0))
    box.x = x
    box.y = y


# Preparation
camera = gamebox.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
player = gamebox.from_color(200, 550, "brown", 20, 20)
platforms = [
    gamebox.from_color(
        rand_platform_x(),
        CAMERA_HEIGHT - VERTICAL_DIST_BTW_PLATFORMS * i,
        "Green",
        PLATFORM_WIDTH, PLATFORM_HEIGHT)
    for i in range(PLATFORM_COUNT)]


# Mainloop
def tick(keys):
    camera.clear("white")

    # Movement of platform:
    for i in range(PLATFORM_COUNT):
        platform = platforms[i]
        platform.move(0, 2)
        if platform.y >= CAMERA_HEIGHT:
            platform.x = rand_platform_x()
            platform.y = platforms[(i + PLATFORM_COUNT - 1) % PLATFORM_COUNT].y - VERTICAL_DIST_BTW_PLATFORMS

    # Movement of player
    if pygame.K_LEFT in keys:
        player.speedx -= PLAYER_X_SPEED_INCREMENT
    if pygame.K_RIGHT in keys:
        player.speedx += PLAYER_X_SPEED_INCREMENT
    player.speedx *= FRICTION
    player.move_speed()

    for platform in platforms:
        camera.draw(platform)
    camera.draw(player)
    camera.display()


# Initiation
gamebox.timer_loop(60, tick)
