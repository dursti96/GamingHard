import pygame as pg


class Character(pg.sprite.Sprite):
    def __init__(self, posx, posy, direction, speed):
        super().__init__()
        self.image_org = pg.image.load(r"src\img\player_img.png")
        self.image = pg.transform.scale(self.image_org, (310, 256)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(posx, posy))
        self.mask = pg.mask.from_surface(self.image)
        self.speed_x = 0
        self.speed_y = 0
        self.direction = direction
        self.posx = posx
        self.posy = posy
        self.speed = speed

    def update_img_rect(self, screen_height, char_size):
        self.image = pg.transform.scale(self.image_org, (
            screen_height * char_size / 1.4, screen_height * char_size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.posx, self.posy))
        self.mask = pg.mask.from_surface(self.image)

    def check_out_of_bounds(self, screen_width, screen_height, stats_screen_height, title_bar_height=31):
        if self.rect.left < 0 and self.speed_x < 0:
            self.speed_x = 0
        if self.rect.right > screen_width and self.speed_x > 0:
            self.speed_x = 0
        if self.rect.top < 0 and self.speed_y < 0:
            self.speed_y = 0
        if self.rect.bottom > screen_height + stats_screen_height + title_bar_height and self.speed_y > 0:
            self.speed_y = 0

    def change_speed(self, event):
        # if key is pressed, adjust speed
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                self.speed_x += - 1 * self.speed
            if event.key == pg.K_d:
                self.speed_x += 1 * self.speed
            if event.key == pg.K_w:
                self.speed_y += - 1 * self.speed
            if event.key == pg.K_s:
                self.speed_y += 1 * self.speed
        # if key is released
        if event.type == pg.KEYUP:
            # if a or d released
            if event.key == pg.K_a or event.key == pg.K_d:
                self.speed_x = 0
            # if w or s released
            if event.key == pg.K_w or event.key == pg.K_s:
                self.speed_y = 0

    def move_rect(self):
        self.posx += self.speed_x * self.rect.width / 100
        self.posy += self.speed_y * self.rect.height / 100
        self.rect.topleft = (self.posx, self.posy)

    def check_direction(self):
        # face right direction; False == face right, True == face left
        if self.speed_x < 0:
            if not self.direction:
                self.image = pg.transform.flip(self.image, True, False)
                self.image_org = pg.transform.flip(self.image_org, True, False)
                self.mask = pg.mask.from_surface(self.image)
                self.direction = True
        if self.speed_x > 0:
            if self.direction:
                self.image = pg.transform.flip(self.image, True, False)
                self.image_org = pg.transform.flip(self.image_org, True, False)
                self.mask = pg.mask.from_surface(self.image)
                self.direction = False
