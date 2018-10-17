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

    def events(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.next_direction = 'left'
            self.direction = 'left'
        if keys[pg.K_RIGHT]:
            self.next_direction = 'right'
            self.direction = 'right'
        if keys[pg.K_UP]:
            self.next_direction = 'up'
            self.direction = 'up'
        if keys[pg.K_DOWN]:
            self.next_direction = 'down'
            self.direction = 'down'

    def update(self):
        if self.game.now - self.update_time > PLAYER['time_to_move']:
            self.update_time = self.game.now
            self.vel = self.convert_direction2vel()
            self.pos += self.vel
        self.events()

    def update_for_draw(self):
        self.rect.topleft = self.pos


def handle_collisions(player, walls):
    print 'handle_collisions'
    player.rect.topleft = player.pos
    hits = pg.sprite.spritecollide(player, walls, False)
    if hits:
        print 'hits', hits, player.direction, player.next_direction
        wall = hits[0]
        if player.direction == 'right':
            player.pos.x = wall.rect.left - player.rect.width
            # if player.direction == player.next_direction:
            #     player.next_direction = 'down'
            # player.direction = player.next_direction
        elif player.direction == 'down':
            player.pos.y = wall.rect.top - player.rect.height
            # if player.direction == player.next_direction:
            #     player.next_direction = 'left'
            # player.direction = player.next_direction
        elif player.direction == 'left':
            player.pos.x = wall.rect.right
            # if player.direction == player.next_direction:
            #     player.next_direction = 'up'
            # player.direction = player.next_direction
        elif player.direction == 'up':
            player.pos.y = wall.rect.bottom
            # if player.direction == player.next_direction:
            #     player.next_direction = 'right'
            # player.direction = player.next_direction
        player.direction = 'stop'


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
        handle_collisions(self.player, self.walls)
        self.player.update_for_draw()

    def draw(self):
        self.screen.fill(SCREEN['BGCOLOR'])
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
