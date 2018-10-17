#!/usr/bin/env python
from os import path
import pygame as pg
from settings import GAME, SCREEN, PLAYER
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER['LAYER']
        self.groups = game.all_sprites
        super(Player, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface((GAME['TILESIZE'], GAME['TILESIZE']))
        self.image.fill(PLAYER['color'])
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.direction = 'up'

        self.rect.topleft = self.pos

    def convert_direction2vel(self):
        converter = {
            'right': (PLAYER['speed'], 0),
            'left': (-PLAYER['speed'], 0),
            'up': (0, -PLAYER['speed']),
            'down': (0, PLAYER['speed'])
        }
        return vec(converter[self.direction])

    def events(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.direction = 'left'
        if keys[pg.K_RIGHT]:
            self.direction = 'right'
        if keys[pg.K_UP]:
            self.direction = 'up'
        if keys[pg.K_DOWN]:
            self.direction = 'down'

    def update(self):
        self.vel = self.convert_direction2vel()
        self.events()
        self.pos += self.vel
        if self.pos.x > SCREEN['WIDTH']:
            self.pos.x = 0
        self.rect.topleft = self.pos


class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN['WIDTH'], SCREEN['HEIGHT']))
        pg.display.set_caption(GAME['NAME'])
        self.clock = pg.time.Clock()

        # variables
        self.cmd_key_down = False

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
        self.player = Player(self, 100, 100)

    def run(self):
        # game loop - set  self.playing = False to end the game
        self.running = True
        while self.running:
            self.clock.tick(SCREEN['FPS'])
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
