import pygame as pg
from settings import *
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")

player_folder = os.path.join(img_folder,"player")

class Graphics:
    def __init__(self):
        self.bird_anim = []
        self.player_init()

    def player_init(self):
        for i in range(1,9):
            filename = 'frame-{}.png'.format(i)
            img = pg.image.load(os.path.join(player_folder, filename)).convert()
            img.set_colorkey(BLACK)
            img_final = pg.transform.scale(img, (70,70))
            self.bird_anim.append(img_final)