# Cell Jump
Game project for CS 1110, modeled after doodle jump

### Optional Features:
1. Animation: the cell is compressed and then reverted when hits a platform
2. Inter-session progress: Highscore displayed at the end
3. Collectibles: jetpacks
4. Scrolling level: it goes without saying that this game can go on indefinitely...

### Authors:
**Derek Habron** (djh5es)
 
**Simeng Hao** (sh4aj)

###Notes:
There are several files the main game depends on:
+ `.highscore.txt` is used to store the top 20 highscores
+ `auxiliary_funcs` defines a number of non-gamebox-dependent helper functions
+ `consts.py` specifies a number of constant used in the game
+ `Jetpack_spritesheet.png` is the spritesheet used to animate jetpacks
+ `SpriteSheet.png` is the spritesheet used to animate the player(the cell)
