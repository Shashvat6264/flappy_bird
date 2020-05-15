# Sprite classes for the platformer game
import pygame as pg
import random
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


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
