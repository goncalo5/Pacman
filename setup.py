#!/usr/bin/env python
from os import path
from random import choice
import pygame as pg
from settings import GAME, SCREEN, WALLS, PLAYER, MOB, PACDOTS, RED
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
        self.update_time2forget = self.game.now

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
            list_of_possibles_moves =\
                remove_inverse_from_possible_moves(
                    self, list_of_possibles_moves)

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
            self.update_time2forget = self.game.now
        if keys[pg.K_RIGHT]:
            self.next_direction = 'right'
            self.update_time2forget = self.game.now
        if keys[pg.K_UP]:
            self.next_direction = 'up'
            self.update_time2forget = self.game.now
        if keys[pg.K_DOWN]:
            self.next_direction = 'down'
            self.update_time2forget = self.game.now

    def update(self):
        self.events()
        if self.game.now - self.update_time2forget >\
                PLAYER['time_to_forget_move']:
            self.update_time2forget = self.game.now
            self.next_direction = None

        if self.game.now - self.update_time > PLAYER['time_to_move']:
            self.update_time = self.game.now

            list_of_possibles_moves =\
                check_possibles_moves(self, self.game.walls)
            if self.next_direction in list_of_possibles_moves:
                self.direction = self.next_direction
            elif self.direction in list_of_possibles_moves:
                pass
            else:
                list_of_possibles_moves =\
                    remove_inverse_from_possible_moves(
                        self, list_of_possibles_moves)
                self.direction = choice(list_of_possibles_moves)

            # collide with PacDot:
            pg.sprite.spritecollide(self, self.game.pacdots, True)

            self.vel = self.convert_direction2vel()
            self.pos += self.vel
            self.update_for_draw()


class PacDot(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PACDOTS['layer']
        self.groups = game.all_sprites, game.pacdots
        super(PacDot, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface(PACDOTS['size'])
        self.image.fill(PACDOTS['color'])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


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
    return list_of_possibles_moves


def remove_inverse_from_possible_moves(animated, list_of_possibles_moves):
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
        self.pacdots = pg.sprite.Group()
        with open('map.txt') as map:
            self.map_list = map.readlines()
            self.width = (len(self.map_list[0]) - 1) * self.tilesize
            self.height = (len(self.map_list)) * self.tilesize
        self.screen = pg.display.set_mode((self.width, self.height))

        for i, line in enumerate(self.map_list):
            for j, value in enumerate(line[:-1]):
                x = j * self.tilesize
                y = i * self.tilesize
                x_center = x + self.tilesize / 2.
                y_center = y + self.tilesize / 2.
                if value == 'w':
                    Wall(self, x, y, self.tilesize, self.tilesize)
                elif value == 'p':
                    self.player = Player(self, x, y)
                elif value == 'm':
                    Mob(self, x, y)
                    PacDot(self, x_center, y_center)
                else:
                    PacDot(self, x_center, y_center)

    def pause(self):
        self.draw_text(self.paused_msg, 50, RED,
                       self.width / 2, self.height / 2, GAME['font'])

    def run(self):
        # game loop - set  self.playing = False to end the game
        self.running = True
        self.paused = False
        self.paused_msg = None
        while self.running:
            self.clock.tick(SCREEN['FPS'])
            self.now = pg.time.get_ticks()
            self.events()
            if not self.paused:
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

            if event.key == pg.K_p:
                self.paused = not self.paused
                self.paused_msg = 'Paused'

        if event.type == pg.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        if not self.pacdots:
            self.paused = not self.paused
            self.paused_msg = 'YOU WIN'

    def draw_text(self, text, size, color, x, y, font='freesansbold.ttf'):
        try:
            font = pg.font.Font(font, size)
        except IOError:
            font = pg.font.SysFont(font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(SCREEN['BGCOLOR'])
        self.all_sprites.draw(self.screen)
        if self.paused:
            self.pause()

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
