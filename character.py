import math
import time

import pygame as pg


class Character(pg.sprite.Sprite):
    def __init__(self, posx, posy, direction):
        super().__init__()
        self.image_org = pg.image.load(r"src/img/player_img.png")
        self.image = pg.transform.scale(self.image_org, (310, 256)).convert_alpha()
        self.rect = self.image.get_rect(center=(posx, posy))
        self.mask = pg.mask.from_surface(self.image)
        self.speed_x = 0
        self.speed_y = 0
        self.direction = direction
        self.posx = posx
        self.posy = posy
        self.speed = 5

    def update_img_rect(self, screen_height, char_size):
        self.image = pg.transform.scale(self.image_org, (
            screen_height * char_size / 1.4, screen_height * char_size)).convert_alpha()
        self.rect = self.image.get_rect(center=(self.posx, self.posy))
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
        self.rect.center = (self.posx, self.posy)

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

    def create_bullet1(self, pos_mouse, height):
        charx = self.rect.center[0]
        chary = self.rect.center[1]
        direction = (pos_mouse[0] - charx, pos_mouse[1] - chary - height)
        length = math.hypot(*direction)
        if length == 0.0:
            direction = (0, -1)
        else:
            direction = (direction[0] / length, direction[1] / length)

        return Bullet1(charx, chary, direction)


class Bullet1(pg.sprite.Sprite):
    def __init__(self, posx, posy, direction):
        super().__init__()
        self.angle = math.degrees(math.atan2(direction[1], direction[0]))
        self.image_org = pg.image.load(r"src/img/player_bullet.png")
        self.image_scaled = pg.transform.scale(self.image_org, (100, 65)).convert_alpha()
        self.image = pg.transform.rotate(self.image_scaled, 360 - self.angle).convert_alpha()
        self.rect = self.image.get_rect(center=(posx, posy))
        self.mask = pg.mask.from_surface(self.image)
        self.direction = direction
        self.posx = posx
        self.posy = posy
        self.speed = 6

    def move(self):
        self.posx = self.posx + self.direction[0] * self.speed
        self.posy = self.posy + self.direction[1] * self.speed
        self.rect.center = (self.posx, self.posy)

    def check_collision(self, enemy_group):
        for enemy in enemy_group:
            if not pg.sprite.collide_mask(self, enemy) is None:
                if self not in enemy.hit_by:
                    enemy.hit_by.append(self)
                    enemy.health -= 1
                    enemy.hit_status = 5

    def check_out_of_bounds(self, bullet1_group, screen_rect):
        if not screen_rect.contains(self.rect):
            bullet1_group.remove(self)

