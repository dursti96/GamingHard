import pygame as pg


class Object(pg.sprite.Sprite):
    def __init__(self, image_link, posx, posy, height, width):
        super().__init__()
        self.image = pg.image.load(image_link)
        self.image = pg.transform.scale(self.image, (height, width)).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(posx, posy))
        self.posx = posx
        self.posy = posy

    def move_rect(self):
        self.rect = self.image.get_rect(midbottom=(self.posx, self.posy))