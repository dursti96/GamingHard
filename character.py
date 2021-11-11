import pygame as pg


class Character(pg.sprite.Sprite):
    def __init__(self, posx, posy, speed_x, speed_y, direction):
        super().__init__()
        self.image = pg.image.load("src\\img\\player_img.png")
        self.image = pg.transform.scale(self.image, (156, 126)).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(posx, posy))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = direction
        self.posx = posx
        self.posy = posy

    def check_out_of_bounds(self, screen_width, screen_height):
        if self.rect.left < 0 and self.speed_x < 0:
            self.speed_x = 0
        if self.rect.right > screen_width and self.speed_x > 0:
            self.speed_x = 0
        if self.rect.top < 0 and self.speed_y < 0:
            self.speed_y = 0
        if self.rect.bottom > screen_height and self.speed_y > 0:
            self.speed_y = 0

    def change_speed(self, event):
        # if key is pressed, adjust speed
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                self.speed_x = - 0.3
            if event.key == pg.K_d:
                self.speed_x = 0.3
            if event.key == pg.K_w:
                self.speed_y = - 0.3
            if event.key == pg.K_s:
                self.speed_y = 0.3
        # if key is released
        if event.type == pg.KEYUP:
            # if a or d released
            if event.key == pg.K_a or event.key == pg.K_d:
                self.speed_x = 0
            # if w or s released
            if event.key == pg.K_w or event.key == pg.K_s:
                self.speed_y = 0

    def move_char_rect(self):
        self.posx += self.speed_x
        self.posy += self.speed_y
        self.rect.midbottom = (self.posx, self.posy)

    def check_direction(self):
        # face right direction; False == face right, True == face left
        if self.speed_x < 0:
            if not self.direction:
                self.image = pg.transform.flip(self.image, True, False)
                self.direction = True
        if self.speed_x > 0:
            if self.direction:
                self.image = pg.transform.flip(self.image, True, False)
                self.direction = False
