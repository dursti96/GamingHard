import math

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
        self.speed = 6
        self.energy = 5
        self.energy_loading = False
        self.energy_loading_time = 0
        self.score = 0
        self.new_high_score = False
        self.name = "user"

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
        self.energy -= 1
        return Bullet1(charx, chary, direction)

    def update_energy(self):
        # get 1 energy evergy 30 frames - 1 sek
        if self.energy < 5 and self.energy_loading is False:
            self.energy_loading = True
            self.energy_loading_time = 30
        if self.energy_loading is True:
            if self.energy_loading_time >= 0:
                self.energy_loading_time -= 1
            else:
                self.energy += 1
                self.energy_loading = False

    def update_energy_img(self, energy_group, energy_full_list, energy_empty_list, stats_screen):

        for energy in energy_full_list:
            energy.rect = energy.image.get_rect(center=(stats_screen.get_width() / 1.5, stats_screen.get_height() / 2))

        for energy in energy_empty_list:
            energy.rect = energy.image.get_rect(center=(stats_screen.get_width() / 1.5, stats_screen.get_height() / 2))

        energy_group.empty()
        empty_energy_count = 5 - self.energy
        energy_count = self.energy
        while energy_count > 0:
            energy_group.add(energy_full_list[energy_count-1])
            energy_count -= 1
        while empty_energy_count > 0:
            energy_group.add(energy_empty_list[empty_energy_count-1])
            empty_energy_count -= 1

        offset = 80
        offset_counter = 0
        for energy in energy_group:
            energy.rect = energy.image.get_rect(center=(energy.rect.center[0] + offset * offset_counter, energy.rect.center[1]))
            offset_counter += 1


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
        self.death_count = 0

    def move(self):
        self.posx += self.direction[0] * self.speed
        self.posy += self.direction[1] * self.speed
        self.rect.center = (self.posx, self.posy)

    def check_collision(self, enemy_group):
        for enemy in enemy_group:
            if not pg.sprite.collide_mask(self, enemy) is None:
                if self not in enemy.hit_by:
                    enemy.hit_by.append(self)
                    enemy.health -= 1
                    enemy.hit_status = 5
                    if enemy.health <= 0:
                        enemy_group.remove(enemy)
                        self.death_count += 1

    def check_out_of_bounds(self, bullet1_group, screen_rect):
        if not screen_rect.contains(self.rect):
            bullet1_group.remove(self)

