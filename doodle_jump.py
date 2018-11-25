# Written by Simeng Hao (sh4aj) and Derek Habron (djh5es)
# Modeled after Doodle Jump
from math import factorial
from random import randint

import pygame

import gamebox

# Key attributes
CAMERA_WIDTH = 400
CAMERA_HEIGHT = 600
PLATFORM_HEIGHT = 10
PLATFORM_WIDTH = 60
VERTICAL_DIST_BTW_PLATFORMS = 100
PLATFORM_COUNT = 6
Y_BASELINE = CAMERA_HEIGHT - 50
PLAYER_X_SPEED_INCREMENT = 3
FRICTION = 0.8
GRAVITY = 0.5
REBOUNCE_SPEED = -15
FRAME_PER_MOVEMENT = 30


# Definitions

def binom(n, p, k):
    def nCr(n, r):
        f = factorial
        return f(n) / (f(n - r) * f(r))

    return nCr(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binom_list(length):
    list = []
    for i in range(length):
        list.append(binom(length, 0.5, i))
    return list


def rand_platform_x():
    return randint(PLATFORM_WIDTH / 2, CAMERA_WIDTH - (PLATFORM_WIDTH / 2) + 1)


def hits_platform(player, platforms):
    """ returns whether the player lands on any of the platforms"""
    for platform in platforms:
        if player.bottom_touches(platform) and player.speedy > 0:
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
    if hits_platform(player, platforms):
        player.speedy = REBOUNCE_SPEED


def create_movement_list(displacement, list):
    for i in range(FRAME_PER_MOVEMENT):
        list.append(displacement * movement_coefficients[i])


def respawn_platforms():
    for i in range(PLATFORM_COUNT):
        platform = platforms[i]
        if platform.y >= CAMERA_HEIGHT:
            platform.x = rand_platform_x()
            platform.y = platforms[(i + PLATFORM_COUNT - 1) % PLATFORM_COUNT].y - VERTICAL_DIST_BTW_PLATFORMS


def scroll_downwards(list):
    try:
        movement = list.pop()
    except IndexError:
        pass
        #movement = 0
    else:
        for object in objects:
            object.move(0, movement)
        respawn_platforms()


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
objects = platforms + [player]
movement_each_frame = []
movement_coefficients = binom_list(FRAME_PER_MOVEMENT)


# Mainloop
def tick(keys):
    camera.clear("white")

    move_player_horizontally(keys)
    move_player_vertically()

    player.move_speed()

    if hits_platform(player, platforms):
        displacement = Y_BASELINE - player.y
        create_movement_list(displacement, movement_each_frame)

    scroll_downwards(movement_each_frame)

    for platform in platforms:
        camera.draw(platform)
    camera.draw(player)
    camera.display()


# Initiation
gamebox.timer_loop(120, tick)
