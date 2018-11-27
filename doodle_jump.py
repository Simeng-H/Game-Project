# Written by Simeng Hao (sh4aj) and Derek Habron (djh5es)
# Modeled after Doodle Jump
from math import factorial
from random import randint

import pygame

import gamebox
from const import *


# Definitions

def binom(n, p, k):
    """
    returns the probability of k positive results out of n tests, where the probability of having a positive result
    in a test is p.
    :param n: int
    :param p: float
    :param k: int
    :return: float
    """

    def nCr(n, r):
        f = factorial
        return f(n) / (f(n - r) * f(r))

    return nCr(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binom_list(length):
    """
    return a list of length n where the elements follows the binomial distribution curve and sums to 1
    :param length: int
    :return: list
    """
    list = []
    for i in range(length):
        list.append(binom(length, 0.5, i))
    return list


def rand_platform_x():
    """
    returns a
    :return: int
    """
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
    else:
        for object in objects:
            object.move(0, movement)
        respawn_platforms()


def draw_highscore(x, y):
    f = open("highscore.txt")
    i = 0
    boxes = []
    for line in f:
        if i >= 10:
            break
        box = gamebox.from_text(x, y + 60 * i,line,25,"white")
        camera.draw(box)
        i += i



def end_screen(score):
    camera.clear("black")
    draw_highscore(80,80)
    camera.display()
    # global


def start_screen(keys):
    global game_started
    camera.clear("White")
    camera.draw("use left and right arrow to move", 30, "black", CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2)
    camera.draw("""press left or right to start""", 30, "black", CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2 + 60)
    camera.display()
    if pygame.K_LEFT in keys or pygame.K_RIGHT in keys:
        game_started = True


def display_scorebox():
    score_box = gamebox.from_text(50, 50, str(score), 30, "Black")
    camera.draw(score_box)
    del score_box


# Preparation
camera = gamebox.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
# player = gamebox.from_color(200, 550, "brown", 20, 20)
player = gamebox.from_image(200, 550, "transparent cell.png")
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
game_started = False
game_lost = False
score = 0
player_height = 0


# Mainloop
def tick(keys):
    global game_started
    global score
    global player_height
    global game_lost

    if not game_started:
        start_screen(keys)

    if game_started:

        camera.clear("white")

        move_player_horizontally(keys)
        move_player_vertically()

        player.move_speed()
        player_height -= player.speedy
        if player_height >= score:
            score = int(player_height)

        if hits_platform(player, platforms):
            displacement = Y_BASELINE - player.y
            # max_height -= displacement
            create_movement_list(displacement, movement_each_frame)

        scroll_downwards(movement_each_frame)

        if pygame.K_SPACE in keys:
            game_lost = True

        for platform in platforms:
            camera.draw(platform)
        # print(score)
        camera.draw(player)
        display_scorebox()
        camera.display()
    if not game_started:
        start_screen(keys)
    if game_lost:
        end_screen(score)
        gamebox.pause()


# Initiation
gamebox.timer_loop(120, tick)
