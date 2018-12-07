# Written by Simeng Hao (sh4aj) and Derek Habron (djh5es)
# Modeled after Doodle Jump

import gamebox
from auxiliary_funcs import *
from const import *
import random


# Definitions
def jetpack_timer():
    global jetpack_active_frames
    global jetpack_active
    #if jetpack_active:
    jetpack_active_frames += 1
    print(jetpack_active_frames)
    if jetpack_active_frames > JETPACK_EFFECTIVE_FRAMES:
        jetpack_active_frames = 0
        del jetpacks[0]
        jetpack_active = False


def handle_collision():
    global frames_to_animate
    global jetpack_active
    if hits_platform(player, platforms):
        displacement = Y_BASELINE - player.y
        create_scroll_movement_list(displacement, movement_each_frame)
        frames_to_animate = 18
    if jetpacks != [] and player.touches(jetpacks[0]):
        jetpack_active = True


def hits_platform(player, platforms):
    """ returns whether the player lands on any of the platforms"""
    for platform in platforms:
        if player.bottom_touches(platform) and player.speedy > 0:
            return True
    return False


def move_player_horizontally(keys):
    if pygame.K_LEFT in keys:
        player.image = player_sprite_sheet[9]
        player.speedx -= PLAYER_X_SPEED_INCREMENT
    elif pygame.K_RIGHT in keys:
        player.image = player_sprite_sheet[10]
        player.speedx += PLAYER_X_SPEED_INCREMENT
    else:
        player.image = player_sprite_sheet[8]
    player.speedx *= FRICTION
    if player.x <= 0:
        player.x += CAMERA_WIDTH
    if player.x > CAMERA_WIDTH:
        player.x -= CAMERA_WIDTH


def move_player_vertically():
    player.speedy += GRAVITY
    if hits_platform(player, platforms):
        player.speedy = REBOUNCE_SPEED
    player.move_speed()
    if jetpack_active:
        #print(jetpack_active)
        jetpacks[0].x = player.x
        jetpacks[0].y = player.y
        jetpacks[0].image = jetpack_sprite_sheet[toggle(2)+1]
        jetpack_timer()
        player.speedy = JETPACK_SPEED
        scroll_downwards([-player.speedy-1])


def move_player(keys):
    move_player_horizontally(keys)
    move_player_vertically()


def animate_player():
    global frames_to_animate
    if frames_to_animate != 0:
        player.image = player_sprite_sheet[abs(9 - frames_to_animate)]
        frames_to_animate -= 1


def create_scroll_movement_list(displacement, list):
    for i in range(FRAME_PER_MOVEMENT):
        list.append(displacement * movement_coefficients[i])


def respawn_platforms():
    for i in range(PLATFORM_COUNT):
        platform = platforms[i]
        if platform.y >= CAMERA_HEIGHT:
            platform.x = rand_platform_x()
            platform.y = platforms[(i + PLATFORM_COUNT - 1) % PLATFORM_COUNT].y - VERTICAL_DIST_BTW_PLATFORMS
            if random.random() < JETPACK_SPAWN_CHANCE and jetpacks == []:
                spawn_jetpack(platform.x, platform.y - 10)


def scroll_downwards(list):
    global jetpack
    try:
        movement = list.pop(0)
    except IndexError:
        pass
    else:
        for object in objects:
            object.move(0, movement)
        respawn_platforms()
        if jetpacks != [] and jetpacks[0].y > CAMERA_HEIGHT:
            del jetpacks[0]


def draw_highscore(x, y, score_list):
    camera.draw("Highscores", FONT_SIZE_2, "white", X_START, Y_START)
    i = 1
    for item in score_list:
        if i >= (ROW_COUNT):
            break
        score_text = "{}. {}".format(i, item)
        box = gamebox.from_text(x, y + VERTICAL_SEP_HIGHSCORE * i, score_text, 25, "white")
        camera.draw(box)
        i += 1


def display_end_screen(score):
    score_list = read_highscore(HIGHSCORE_PATH)
    insert_into_highscore(score, score_list)
    camera.clear("black")
    draw_highscore(X_START, Y_START, score_list)
    update_highscore(HIGHSCORE_PATH, score_list)


def display_start_screen(keys):
    """draws the start screen"""
    global game_started
    camera.clear("White")
    camera.draw("Cell Jump", 50, "black", CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2 - 150)
    camera.draw("Created by:", 30, "black", CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2 - 60)
    camera.draw("Derek Habron (djh5es)", 30, "black", CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2 - 20)
    camera.draw("Simeng Hao (sh4aj)", 30, "black", CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2 + 20)
    camera.draw("use left and right arrow to move", 30, "black", CAMERA_WIDTH / 2, CAMERA_HEIGHT - 60)
    camera.draw("""press left or right to start""", 30, "black", CAMERA_WIDTH / 2, CAMERA_HEIGHT - 100)
    if pygame.K_LEFT in keys or pygame.K_RIGHT in keys:
        game_started = True


def update_score():
    """increments score if the player reaches a new height"""
    global score
    global player_height
    player_height -= player.speedy
    if player_height >= score:
        score = int(player_height)


def display_scorebox():
    """draws scorebox after updating score"""
    update_score()
    score_box = gamebox.from_text(50, 50, str(score), 30, "Black")
    camera.draw(score_box)
    del score_box


def spawn_jetpack(x, y):
    jetpack = gamebox.from_image(x, y, jetpack_sprite_sheet[0])
    jetpacks.append(jetpack)
    objects.append(jetpack)


def draw_collection(collection):
    for item in collection:
        camera.draw(item)


# Preparation

camera = gamebox.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
player_sprite_sheet = gamebox.load_sprite_sheet(SPRITESHEET_PATH, SPRITESHEET_ROW_COUNT, SPRITESHEET_COLUMN_COUNT)
# 0-8 in increasing size, 9 and 10 for left and right
jetpack_sprite_sheet = gamebox.load_sprite_sheet("Jetpack_spritesheet.png", 1, 3)

player = gamebox.from_image(200, 550, player_sprite_sheet[8])
player.speedy = -20
platforms = [
    gamebox.from_color(
        rand_platform_x(),
        CAMERA_HEIGHT - VERTICAL_DIST_BTW_PLATFORMS * i,
        "Green",
        PLATFORM_WIDTH, PLATFORM_HEIGHT)
    for i in range(PLATFORM_COUNT)]
jetpacks = []
jetpack_active = False
jetpack_active_frames = 0
objects = platforms + [player]
movement_each_frame = []
movement_coefficients = binom_list(FRAME_PER_MOVEMENT)
game_started = False
game_lost = False
score = 0
player_height = 0
frames_to_animate = 0


# Mainloop
def tick(keys):
    global game_started
    global score
    global player_height
    global game_lost

    if game_started and not game_lost:

        camera.clear("white")

        move_player(keys)

        animate_player()

        handle_collision()

        scroll_downwards(movement_each_frame)

        if player.y >= CAMERA_HEIGHT:
            game_lost = True

        draw_collection(platforms)
        draw_collection(jetpacks)
        camera.draw(player)
        display_scorebox()
    elif not game_started:
        display_start_screen(keys)
    elif game_lost:
        display_end_screen(score)
        gamebox.pause()

    camera.display()


# Initiation
gamebox.timer_loop(60, tick)
