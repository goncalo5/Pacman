#!/usr/bin/env python
from os import path
from random import choice
import pygame as pg
from settings import GAME, SCREEN, WALLS, PLAYER, MOB
vec = pg.math.Vector2


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = WALLS['layer']
        self.groups = game.all_sprites, game.walls
        super(Wall, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface((width, height))
        self.image.fill(WALLS['color'])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Animated(pg.sprite.Sprite):
    def __init__(self, game, x, y, group, groups):
        self._layer = group['layer']
        self.groups = groups
        super(Animated, self).__init__(self.groups)
        self.game = game
        self.group = group
        self.image = pg.Surface((GAME['TILESIZE'], GAME['TILESIZE']))
        self.image.fill(group['color'])
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.direction = 'right'
        self.next_direction = 'down'
        self.update_time = self.game.now

        self.rect.topleft = self.pos

    def convert_direction2vel(self):
        converter = {
            'right': (self.game.tilesize, 0),
            'left': (-self.game.tilesize, 0),
            'up': (0, -self.game.tilesize),
            'down': (0, self.game.tilesize),
            'stop': (0, 0)
        }
        return vec(converter[self.direction])

    def update(self):
        if self.game.now - self.update_time > self.group['time_to_move']:
            self.update_time = self.game.now
            list_of_possibles_moves =\
                check_possibles_moves(self, self.game.walls)
            self.direction = choice(list_of_possibles_moves)
            self.vel = self.convert_direction2vel()
            self.pos += self.vel
            self.update_for_draw()

    def update_for_draw(self):
        self.rect.topleft = self.pos


class Mob(Animated):
    def __init__(self, game, x, y):
        groups = game.all_sprites, game.mobs
        super(Mob, self).__init__(game, x, y, MOB, groups)


class Player(Animated):
    def __init__(self, game, x, y):
        groups = game.all_sprites
        super(Player, self).__init__(game, x, y, PLAYER, groups)

    def events(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.next_direction = 'left'
            # self.direction = 'left'
        if keys[pg.K_RIGHT]:
            self.next_direction = 'right'
            # self.direction = 'right'
        if keys[pg.K_UP]:
            self.next_direction = 'up'
            # self.direction = 'up'
        if keys[pg.K_DOWN]:
            self.next_direction = 'down'
            # self.direction = 'down'

    def update(self):
        self.events()
        if self.game.now - self.update_time > PLAYER['time_to_move']:
            self.update_time = self.game.now

            list_of_possibles_moves =\
                check_possibles_moves(self, self.game.walls)
            self.direction = choice(list_of_possibles_moves)
            if self.next_direction in list_of_possibles_moves:
                self.direction = self.next_direction
            self.vel = self.convert_direction2vel()
            self.pos += self.vel
            self.update_for_draw()

#####################################################
# Collisions:
#


def check_possibles_moves(animated, walls):
    list_of_possibles_moves = []
    # check up:
    animated.rect.y -= 1
    if not pg.sprite.spritecollide(animated, walls, False):
        list_of_possibles_moves.append('up')
    animated.rect.y += 1
    # check down:
    animated.rect.y += 1
    if not pg.sprite.spritecollide(animated, walls, False):
        list_of_possibles_moves.append('down')
    animated.rect.y -= 1
    # check right:
    animated.rect.x += 1
    if not pg.sprite.spritecollide(animated, walls, False):
        list_of_possibles_moves.append('right')
    animated.rect.x -= 1
    # check left:
    animated.rect.x -= 1
    if not pg.sprite.spritecollide(animated, walls, False):
        list_of_possibles_moves.append('left')
    animated.rect.x += 1

    try:
        list_of_possibles_moves.remove(
            convert_direction_to_inverse(animated.direction))
    except ValueError:
        print 123
        pass
    return list_of_possibles_moves


def remove_self_direction(animated, list_of_possibles_moves):

    try:
        list_of_possibles_moves.remove(animated.direction)
    except ValueError:
        pass
    return list_of_possibles_moves


def convert_direction_to_inverse(direction):
    if direction == 'left':
        return 'right'
    if direction == 'right':
        return 'left'
    if direction == 'down':
        return 'up'
    if direction == 'up':
        return 'down'

#
# End of Collisions
####################################################


class Game(object):
    def __init__(self):
        pg.init()
        # variables
        self.tilesize = GAME['TILESIZE']
        # self.width = SCREEN['WIDTH']
        # self.height = SCREEN['HEIGHT']
        self.cmd_key_down = False

        pg.display.set_caption(GAME['NAME'])
        self.clock = pg.time.Clock()
        self.now = pg.time.get_ticks()

        self.load_data()
        self.new()
        self.run()

        pg.quit()

    def load_data(self):
        self.dir = path.dirname(__file__)
        pg.mixer.init()  # for sound

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        with open('map.txt') as map:
            self.map_list = map.readlines()
            self.width = (len(self.map_list[0]) - 1) * self.tilesize
            self.height = (len(self.map_list)) * self.tilesize
        self.screen = pg.display.set_mode((self.width, self.height))

        for i, line in enumerate(self.map_list):
            for j, value in enumerate(line[:-1]):
                x = j * self.tilesize
                y = i * self.tilesize
                if value == 'w':
                    Wall(self, x, y, self.tilesize, self.tilesize)
                elif value == 'p':
                    self.player = Player(self, x, y)
                elif value == 'm':
                    Mob(self, x, y)

    def run(self):
        # game loop - set  self.playing = False to end the game
        self.running = True
        while self.running:
            self.clock.tick(SCREEN['FPS'])
            self.now = pg.time.get_ticks()
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            self.handle_common_events(event)

    def handle_common_events(self, event):
        # check for closing window
        if event.type == pg.QUIT:
            # force quit
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == 310:
                self.cmd_key_down = True
            if self.cmd_key_down and event.key == pg.K_q:
                # force quit
                quit()

        if event.type == pg.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(SCREEN['BGCOLOR'])
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
