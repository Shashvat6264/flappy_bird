# Sprite classes for the platformer game
import pygame as pg
import random
from settings import *
from graphics import *

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.g = Graphics()
        self.image = pg.Surface((70,70))
        self.image = self.g.bird_anim[0]
        self.frame = 0
        self.frame_rate = 500
        self.last_update = pg.time.get_ticks()
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame += 1
            if self.frame == len(self.g.bird_anim):
                self.frame = 0
            else: 
                center = self.rect.center
                self.image = self.g.bird_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, random.randint(HEIGHT/4,HEIGHT*3/4)))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.randint(HEIGHT/10,HEIGHT*9/10)
        self.velx = 10 
        self.game = game

    def update(self):
        if self.rect.x > 0:
            self.rect.x -= self.velx
        else:
            m = Mob(self.game, WIDTH)
            self.game.all_sprites.add(m)
            self.game.mobs.add(m)
            self.kill()
            self.game.score += 1
