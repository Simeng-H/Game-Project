# Written by Simeng Hao (sh4aj) and Derek Habron (hjb5ek)
from random import randint

import pygame

import gamebox

# Key attributes
PLATFORM_HEIGHT = 10
PLATFORM_WIDTH = 60
VERTICAL_DIST_BTW_PLATFORMS = 100
PLATFORM_COUNT = 6
PLATFORM_BASELINE_Y_POS = 50
PLAYER_X_SPEED_INCREMENT = 5
FRICTION = 0.7
GRAVITY = 0.5
REBOUNCE_SPEED = -15
CAMERA_WIDTH = 400
CAMERA_HEIGHT = 600
FRAME_PER_MOVEMENT = 10


# Definitions:
def rand_platform_x():
    return randint(PLATFORM_WIDTH / 2, CAMERA_WIDTH - (PLATFORM_WIDTH / 2) + 1)


# Preparation
camera = gamebox.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
player = gamebox.from_color(200, 550, "brown", 20, 20)
player.speedy = -20
platforms = [
    gamebox.from_color(
        rand_platform_x(),
        CAMERA_HEIGHT - VERTICAL_DIST_BTW_PLATFORMS * i,
        "Green",
        PLATFORM_WIDTH, PLATFORM_HEIGHT)
    for i in range(PLATFORM_COUNT)]

def hits_platform(player, platforms):
    """ returns whether the player lands on any of the platforms"""
    for platform in platforms:
        if player.bottom_touches(platform) and player.speedy>0:
            return True
    return False

def move_player_horizontally(keys):
    if pygame.K_LEFT in keys:
        player.speedx -= PLAYER_X_SPEED_INCREMENT
    if pygame.K_RIGHT in keys:
        player.speedx += PLAYER_X_SPEED_INCREMENT
    player.speedx *= FRICTION
    if player.x <= 0:
        player.x += CAMERA_WIDTH
    if player.x > CAMERA_WIDTH:
        player.x -= CAMERA_WIDTH


def move_player_vertically():
    player.speedy += GRAVITY
    if hits_platform(player,platforms):
        player.speedy = REBOUNCE_SPEED


def divide_int_into_list(numerator, denominator, list):
    remainder = numerator % denominator
    center = denominator // 2
    start = center - remainder // 2
    end = center + (remainder - remainder // 2)
    sum = 0
    for i in range(denominator):
        list.append(numerator // denominator)
    for i in range(start, end):
        list[i] += 1





movement_each_frame = []


def scroll_downwards(displacement):
    pass


# Mainloop
def tick(keys):
    camera.clear("white")
    rebounced = False

    move_player_horizontally(keys)
    move_player_vertically()

    player.move_speed()

    # Movement of platform:
    if rebounced:
        for i in range(PLATFORM_COUNT):
            platform = platforms[i]
            # platform.move(0, displacement)
            if platform.y >= CAMERA_HEIGHT:
                platform.x = rand_platform_x()
                platform.y = platforms[(i + PLATFORM_COUNT - 1) % PLATFORM_COUNT].y - VERTICAL_DIST_BTW_PLATFORMS
        rebounced = False

    for platform in platforms:
        camera.draw(platform)
    camera.draw(player)
    camera.display()


# Initiation
gamebox.timer_loop(60, tick)
