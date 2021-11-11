import pygame as pg

from character import Character

pg.init()

# create full screen surface
screen = pg.display.set_mode((1200, 800), pg.RESIZABLE)
# set title, icon
pg.display.set_caption("GamingHard",)
icon = pg.image.load("src\\img\\logo.png")
pg.display.set_icon(icon)
background_rgb = (230, 230, 230)

# level surface
ingame_screen = pg.Surface((screen.get_width(), screen.get_height()/8*7))
ig_background_rgb = (255, 255, 255)

# stats surface
stats_screen = pg.Surface((screen.get_width(), screen.get_height()/8))
stats_background_rgb = (230, 230, 230)

# define player attributes, resize and convert player img
standard_pos_x = ingame_screen.get_width() / 4
standard_pos_y = ingame_screen.get_height() / 1.3

standard_x_speed = 0
standard_y_speed = 0
# 0 is right
standard_direction = False

# create character
char = Character(standard_pos_x, standard_pos_y, standard_x_speed, standard_y_speed, standard_direction)

# game loop
running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        char.change_speed(event)

    # fill screen background, neccessary if screen size changes
    ingame_screen = pg.Surface((screen.get_width(), screen.get_height() / 8 * 7))
    stats_screen = pg.Surface((screen.get_width(), screen.get_height() / 8))
    screen.fill(background_rgb)
    ingame_screen.fill(ig_background_rgb)
    stats_screen.fill(stats_background_rgb)

    # move character
    char.check_out_of_bounds(ingame_screen.get_width(), ingame_screen.get_height())
    char.check_direction()
    char.move_char_rect()

    # blit everything needed
    ingame_screen.blit(char.image, char.rect)
    screen.blit(ingame_screen, (0, screen.get_height()/8))
    screen.blit(stats_screen, (0, 0))

    # update screen
    pg.display.update()
