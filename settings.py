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
    'FPS': 30,
    'BGCOLOR': DARKBLUE
}

# Player
PLAYER = {
    'LAYER': 2,
    'color': YELLOW,
    'speed': 10
}


# Walls:
WALLS = {
    'layer': 2,
    'color': GREEN
}
