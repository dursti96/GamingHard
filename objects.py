import pygame as pg


class Object(pg.sprite.Sprite):
    def __init__(self, image_link, posx, posy, height, width):
        super().__init__()
        self.image_org = pg.image.load(image_link)
        self.image = pg.transform.scale(self.image_org, (height, width)).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(posx, posy))
        self.posx = posx
        self.posy = posy

    def move_rect(self):
        self.rect = self.image.get_rect(midbottom=(self.posx, self.posy))

    def update_object_rect(self, screen_height, screen_width, size, posy):
        self.image = pg.transform.scale(self.image_org, (
            screen_width * 2.1 * size, screen_height * size)).convert_alpha()
        self.posx = screen_width / 2
        self.posy = screen_height / posy
