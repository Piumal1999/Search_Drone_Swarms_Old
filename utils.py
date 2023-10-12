from constants import *
import pygame as pg
from math import pi, floor
import random
import copy
vec = pg.math.Vector2


def random_color():
    """"
        Picks a random color R,G or B

        :return: color picked
        :rtype : tuple
    """
    a = random.uniform(0, 255)
    rgbl = [a, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


class Aircraft(pg.sprite.Sprite):
    """
        Represents a simple visual animated drone 
        Can load sprites, rotate and update animation
    """

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sprites = []

        for i in range(0, 4):
            self.sprites.append(pg.image.load(
                f'models/Drone/sprite_{i}.png').convert())

        self.atual = 0
        # inherited from the pygame sprite class it is the first element of the drone
        self.image = self.sprites[self.atual]
        # scales down drone sprites to (70,70)
        self.image = pg.transform.scale(
            self.image, (SIZE_DRONE*2, SIZE_DRONE*2))
        # rect is inherited from Sprite
        # defines the sprite's position on the screen
        # take the image size
        self.rect = self.image.get_rect()

        # pega o canto superior esquerdo, posição qualquer
        # self.rect.topleft = 100,100

    def colorize(self, newColor=(40, 40, 40)):
        """
        Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
        original).
        :param image: Surface to create a colorized copy of
        :param newColor: RGB color to use (original alpha values are preserved)
        :return: New colorized Surface instance
        """
        image = self.image.copy()

        # zero out RGB values
        # image.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
        # add in new RGB values
        image.fill(newColor[0:3] + (0,), None, pg.BLEND_RGBA_ADD)
        self.image = image

    def update(self, position, angle, size=SIZE_DRONE * PIX2M):

        # animation update speed is controle by this parameter
        self.atual += 1

        if self.atual >= len(self.sprites):
            self.atual = 0

        self.image = self.sprites[floor(self.atual)]

        # Rotates image -> angle should be in degrees
        # rotozoom(Surface, angle, scale) -> Surface
        self.image = pg.transform.rotozoom(self.image, -angle*180/pi - 90, .12)
        self.rect = self.image.get_rect()
        # positions center of rect in acual drone position
        self.rect.center = position.x, position.y


class Npc_target(pg.sprite.Sprite):
    """
        Represents a simple visual animated tree 
        Can load sprites, rotate and update animation
    """

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sprites = []

        # for i in range(1,4):
        self.sprites.append(pg.image.load(
            f'models/texture/wandering_trader1.png').convert())
        self.sprites[-1] = pg.transform.rotozoom(self.sprites[-1], 0, 1)

        self.atual = 0
        # inherited from the pygame sprite class it is the first element of the drone
        self.image = self.sprites[self.atual]
        # scales down drone sprites to (70,70)
        # self.image = pg.transform.scale(self.image,(RADIUS_OBSTACLES,RADIUS_OBSTACLES))
        # rect is inherited from Sprite
        # defines the sprite's position on the screen
        # take the image size
        self.rect = self.image.get_rect()

        # pega o canto superior esquerdo, posição qualquer
        # self.rect.topleft = 100,100

    def update(self, position, angle, size=SIZE_DRONE * PIX2M):

        # animation update speed is controle by this parameter
        self.atual += .001
        if self.atual >= len(self.sprites)-1:
            self.atual = 0

        self.image = self.sprites[round(self.atual)]

        # Rotates image -> angle should be in degrees
        # rotozoom(Surface, angle, scale) -> Surface
        # self.image = pg.transform.rotozoom(self.image, 0, .2)
        self.rect = self.image.get_rect()
        # positions center of rect in acual drone position
        self.rect.midbottom = position.x, position.y+20


class Tree(pg.sprite.Sprite):
    """
        Represents a simple visual animated tree 
        Can load sprites, rotate and update animation
    """

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sprites = []

        for i in range(1, 9):
            self.sprites.append(pg.image.load(
                f'models/tree3/tree_{i}.png').convert())
            self.sprites[i-1] = pg.transform.rotozoom(self.sprites[i-1], 0, .3)

        self.atual = 0
        # inherited from the pygame sprite class it is the first element of the drone
        self.image = self.sprites[self.atual]
        # scales down drone sprites to (70,70)
        # self.image = pg.transform.scale(self.image,(RADIUS_OBSTACLES,RADIUS_OBSTACLES))
        # rect is inherited from Sprite
        # defines the sprite's position on the screen
        # take the image size
        self.rect = self.image.get_rect()

        # pega o canto superior esquerdo, posição qualquer
        # self.rect.topleft = 100,100

    def update(self, position, angle, size=SIZE_DRONE * PIX2M):

        # animation update speed is controle by this parameter
        self.atual += .001
        if self.atual >= len(self.sprites)-1:
            self.atual = 0

        self.image = self.sprites[round(self.atual)]

        # Rotates image -> angle should be in degrees
        # rotozoom(Surface, angle, scale) -> Surface
        # self.image = pg.transform.rotozoom(self.image, 0, .2)
        self.rect = self.image.get_rect()
        # positions center of rect in acual drone position
        self.rect.midbottom = position.x, position.y+20
