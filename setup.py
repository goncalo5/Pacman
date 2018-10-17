#!/usr/bin/env python
from os import path
import pygame as pg
from settings import GAME, SCREEN, PLAYER, WALLS
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
        self.direction = 'right'
        self.next_direction = 'down'

        self.rect.topleft = self.pos

    def convert_direction2vel(self):
        converter = {
            'right': (PLAYER['speed'], 0),
            'left': (-PLAYER['speed'], 0),
            'up': (0, -PLAYER['speed']),
            'down': (0, PLAYER['speed']),
            'stop': (0, 0)
        }
        return vec(converter[self.direction])

    def events(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.direction not in ['right', 'left']:
            self.next_direction = 'left'
            self.direction = 'left'
        if keys[pg.K_RIGHT] and self.direction not in ['right', 'left']:
            self.next_direction = 'right'
            self.direction = 'right'
        if keys[pg.K_UP] and self.direction not in ['up', 'down']:
            self.next_direction = 'up'
            self.direction = 'up'
        if keys[pg.K_DOWN] and self.direction not in ['up', 'down']:
            self.next_direction = 'down'
            self.direction = 'down'

    def update(self):
        self.vel = self.convert_direction2vel()
        self.events()
        self.pos += self.vel
        if self.pos.x > self.game.width:
            self.pos.x = 0
        self.rect.topleft = self.pos


def handle_collisions(player, walls):
    hits = pg.sprite.spritecollide(player, walls, False)
    if hits:
        print hits, player.direction, player.next_direction
        wall = hits[0]
        if player.direction == 'right':
            player.pos.x = wall.rect.left - player.rect.width
            if player.direction != player.next_direction:
                pass
            else:
                player.next_direction = 'down'
            player.direction = player.next_direction
        elif player.direction == 'down':
            player.pos.y = wall.rect.top - player.rect.height
            if player.direction != player.next_direction:
                pass
            else:
                player.next_direction = 'left'
            player.direction = player.next_direction
        elif player.direction == 'left':
            player.pos.x = wall.rect.right
            if player.direction != player.next_direction:
                pass
            else:
                player.next_direction = 'up'
            player.direction = player.next_direction
        elif player.direction == 'up':
            player.pos.y = wall.rect.bottom
            if player.direction != player.next_direction:
                pass
            else:
                player.next_direction = 'right'
            player.direction = player.next_direction


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
        with open('map.txt') as map:
            self.map_list = map.readlines()
            self.width = (len(self.map_list[0]) - 1) * self.tilesize
            self.height = (len(self.map_list)) * self.tilesize
        self.screen = pg.display.set_mode((self.width, self.height))

        for i, line in enumerate(self.map_list):
            for j, value in enumerate(line[:-1]):
                if value == 'w':
                    Wall(self, j * self.tilesize, i * self.tilesize,
                         self.tilesize, self.tilesize)
        self.player = Player(self, 100, 100)
        # Wall(self, 0, 0, self.width, self.tilesize)
        # Wall(self, 0, self.height - self.tilesize, self.width, self.tilesize)
        # Wall(self, 0, self.tilesize,
        #      self.tilesize, self.height - 2 * self.tilesize)
        # Wall(self, self.width - self.tilesize, self.tilesize,
        #      self.tilesize, self.height - 2 * self.tilesize)

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
        handle_collisions(self.player, self.walls)

    def draw(self):
        self.screen.fill(SCREEN['BGCOLOR'])
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
