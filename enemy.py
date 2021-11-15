from random import randint

import pygame as pg


def get_spawn_pos():
    spawn_direction = randint(0,3)
    # spawn left of screen
    if spawn_direction == 0:
        return -50, randint(100, 900)
    # spawn top of screen
    if spawn_direction == 1:
        return randint(100, 1500), -90
    # spawn right of screen
    if spawn_direction == 2:
        return 1800, randint(100, 900)
    # spawn bottom of screen
    if spawn_direction == 3:
        return randint(100, 1500), 1070


class EnemyFlyman(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_org = pg.image.load(r"src\img\flyMan_fly.png")
        self.image = pg.transform.scale(self.image_org, (310, 256)).convert_alpha()
        self.posx, self.posy = get_spawn_pos()

        self.rect = self.image.get_rect(topleft=(self.posx, self.posy))
        self.speed = randint(15, 30) / 100

    def chase(self, character):
        # move along x
        if self.posx > character.posx:
            self.posx -= self.speed
        elif self.posx < character.posx:
            self.posx += self.speed
        # move along y
        if self.posy < character.posy:
            self.posy += self.speed
        elif self.posy > character.posy:
            self.posy -= self.speed
        self.rect.topleft = (self.posx, self.posy)




