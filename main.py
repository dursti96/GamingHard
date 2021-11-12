import pygame as pg

from character import Character
from objects import Object

pg.init()

# create full screen surface
screen = pg.display.set_mode((1200, 800), pg.RESIZABLE)
# set title, icon
pg.display.set_caption("GamingHard",)
icon = pg.image.load("src\\img\\logo.png")
pg.display.set_icon(icon)
background_rgb = (230, 230, 230)

# menu, ingame, stats
menu_screen = pg.Surface((screen.get_width(), screen.get_height()))
menu_background_rgb = (255, 255, 255)
ingame_screen = pg.Surface((screen.get_width(), screen.get_height()/8*7))
ig_background_rgb = (255, 255, 255)
stats_screen = pg.Surface((screen.get_width(), screen.get_height()/8))
stats_background_rgb = (230, 230, 230)

# define player attributes, resize and convert player img
standard_pos_x = ingame_screen.get_width() / 4
standard_pos_y = ingame_screen.get_height() / 1.3

# game_level 0 == menu, game_level 1 == in level
game_level = 0

standard_x_speed = 0
standard_y_speed = 0
# 0 is right
standard_direction = False
size = 0.20

# create character
char = Character(standard_pos_x, standard_pos_y, standard_x_speed, standard_y_speed, standard_direction)
char.image = pg.transform.scale(char.image, (
            screen.get_height() * size / 1.4, screen.get_height() * size)).convert_alpha()

# create start button
start_button = Object("src/img/button_start.png", screen.get_width()/2, screen.get_height()/2, 100, 100)
start_button_size = 0.2
start_button.image = pg.transform.scale(start_button.image, (
        screen.get_width() * 2.1 * start_button_size, screen.get_width() * start_button_size)).convert_alpha()

# create exit button
exit_button = Object("src/img/button_exit.png", screen.get_width()/2, screen.get_height() / 1.2, 100, 100)
exit_button_size = 0.1
exit_button.image = pg.transform.scale(exit_button.image, (
        screen.get_width() * 2.1 * exit_button_size, screen.get_width() * exit_button_size)).convert_alpha()

# create menu background image
background_menu_img = pg.image.load("src/img/background_menu.jpg")
background_menu_img = pg.transform.scale(background_menu_img, (
        menu_screen.get_height()*2.66, menu_screen.get_height())).convert_alpha()

# game loop
running = True


while running:

    # if screen size is altered
    ingame_screen = pg.Surface((screen.get_width(), screen.get_height() / 8 * 7))
    stats_screen = pg.Surface((screen.get_width(), screen.get_height() / 8))
    menu_screen = pg.Surface((screen.get_width(), screen.get_height()))
    screen.fill(background_rgb)
    ingame_screen.fill(ig_background_rgb)
    stats_screen.fill(stats_background_rgb)
    menu_screen.fill(menu_background_rgb)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # if in menu, and left mouse is clicked, check if click collides with rect of button
        if game_level == 0:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                if button_start_location.collidepoint(pos):
                    game_level = 1
                if button_exit_location.collidepoint(pos):
                    running = False
        if game_level == 1:
            char.change_speed(event)
        # if screen size changes
        if event.type == pg.VIDEORESIZE:
            # set char size
            char.image = pg.transform.scale(char.image, (
            screen.get_width() * size, screen.get_height() / 3 * 2 * size)).convert_alpha()
            # set start button size and position
            start_button.image = pg.transform.scale(start_button.image, (
            screen.get_width() * 2.1 * start_button_size, screen.get_height() * start_button_size)).convert_alpha()
            start_button.posx = screen.get_width()/2
            start_button.posy = screen.get_height()/2
            # set exit button size and position
            exit_button.image = pg.transform.scale(exit_button.image, (
                screen.get_width() * 2.1 * exit_button_size, screen. get_height() * exit_button_size)).convert_alpha()
            exit_button.posx = screen.get_width() / 2
            exit_button.posy = screen.get_height() / 1.2
            # set background image size
            if screen.get_height() * 2.66 < screen.get_width():
                background_menu_img = pg.transform.scale(background_menu_img, (
                    screen.get_width(), screen.get_width() / 2.66)).convert_alpha()
            else:
                background_menu_img = pg.transform.scale(background_menu_img, (
                    screen.get_height() * 2.66, screen.get_height())).convert_alpha()

    # menu
    if game_level == 0:
        menu_screen.blit(background_menu_img, (0, 0))
        start_button.move_rect()
        button_start_location = menu_screen.blit(start_button.image, start_button.rect)
        exit_button.move_rect()
        button_exit_location = menu_screen.blit(exit_button.image, exit_button.rect)
        screen.blit(menu_screen, (0, 0))

    # ingame lvl 1
    if game_level == 1:
        ingame_screen.blit(char.image, char.rect)
        # move character
        char.check_out_of_bounds(ingame_screen.get_width(), ingame_screen.get_height())
        char.check_direction()
        char.move_rect()
        screen.blit(ingame_screen, (0, screen.get_height() / 8))
        screen.blit(stats_screen, (0, 0))

    # update screen
    pg.display.update()


