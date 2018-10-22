#!/usr/bin/env python
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 100)
YELLOW = (255, 255, 0)

# Game
GAME = {
    'NAME': "My Game",
    'TILESIZE': 32,
    'font': 'comicsansms'
}


# Screen
SCREEN = {
    # 'WIDTH': 360,
    # 'HEIGHT': 480,
    'FPS': 60,
    'BGCOLOR': DARKBLUE
}

# Walls:
WALLS = {
    'layer': 2,
    'color': GREEN
}

# Player
PLAYER = {
    'layer': 2,
    'color': YELLOW,
    'time_to_move': 200,
    'time_to_forget_move': 2000
}

# Mobs:
MOB = {
    'layer': 3,
    'color': RED,
    'time_to_move': 1000
}

PACDOTS = {
    'layer': 1,
    'color': WHITE,
    'size': (5, 5)
}
