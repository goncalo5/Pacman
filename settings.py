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
    'TILESIZE': 32
}


# Screen
SCREEN = {
    # 'WIDTH': 360,
    # 'HEIGHT': 480,
    'FPS': 60,
    'BGCOLOR': DARKBLUE
}

# Player
PLAYER = {
    'layer': 2,
    'color': YELLOW,
    'time_to_move': 300,
    'time_to_forget_move': 2000
}

# Mobs:
MOB = {
    'layer': 2,
    'color': RED,
    'time_to_move': 1000
}

# Walls:
WALLS = {
    'layer': 2,
    'color': GREEN
}
