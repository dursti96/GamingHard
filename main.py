import pygame as pg

from character import Character
from enemy import EnemyFlyman
from objects import Object

# create full screen surface
screen = pg.display.set_mode((1600, 1000))
# set title, icon
pg.display.set_caption("GamingHard")
icon = pg.image.load(r"src\img\logo.png")
pg.display.set_icon(icon)
background_rgb = (230, 230, 230)

# menu, ingame, stats
menu_screen = pg.Surface((screen.get_width(), screen.get_height()))
menu_background_rgb = (255, 255, 255)
ingame_screen = pg.Surface((screen.get_width(), screen.get_height() / 8 * 7))
ig_background_rgb = (255, 255, 255)
stats_screen = pg.Surface((screen.get_width(), screen.get_height() / 8))
stats_background_rgb = (230, 230, 230)

# game_level 0 == menu, game_level 1 == in level
game_level = 0

# create character
standard_pos_x = ingame_screen.get_width() / 2
standard_pos_y = ingame_screen.get_height() / 1.5
standard_speed = 2
char = Character(standard_pos_x, standard_pos_y, False, standard_speed)
char_size = 0.10
char.update_img_rect(screen.get_height(), char_size)
# add char to group_single
char_group = pg.sprite.GroupSingle()
char_group.add(char)
bullet1_group = pg.sprite.Group()

# create start button
start_button = Object(r"src/img/button_start.png", screen.get_width() / 2, screen.get_height() / 2, 100, 100)
start_button_size = 0.2
start_button.image = pg.transform.scale(start_button.image, (
    screen.get_width() * 2.1 * start_button_size, screen.get_width() * start_button_size)).convert_alpha()

# create exit button
exit_button = Object(r"src/img/button_exit.png", screen.get_width() / 2, screen.get_height() / 1.2, 100, 100)
exit_button_size = 0.1
exit_button.image = pg.transform.scale(exit_button.image, (
    screen.get_width() * 2.1 * exit_button_size, screen.get_width() * exit_button_size)).convert_alpha()

# create menu background image
background_menu_img = pg.image.load(r"src/img/background_menu.jpg")
background_menu_img = pg.transform.scale(background_menu_img, (
    menu_screen.get_height() * 2.66, menu_screen.get_height())).convert_alpha()

# create death screen image
deathscreen_img = pg.image.load(r"src/img/deathscreen.jpg")
deathscreen_img = pg.transform.scale(deathscreen_img, (
    menu_screen.get_height() * 1.77, menu_screen.get_height())).convert_alpha()

# enemies
flyman_size = 0.15
enemy_group = pg.sprite.Group()

pg.init()

# game loop
running = True
clock = pg.time.Clock()
while running:

    # FPS = 60
    clock.tick(60)

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
        if game_level == "dead":
            if event.type == pg.K_SPACE or event.type == pg.K_ESCAPE:
                enemy_group.empty()
                char = Character(standard_pos_x, standard_pos_y, False, standard_speed)
                char.update_img_rect(screen.get_height(), char_size)
                game_level = 0
        if game_level == 1:
            # character move, shoot bullet
            char.change_speed(event)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                print(pos)
                print(char.rect.center)
                print("-")
                bullet1_group.add(char.create_bullet1(pos))
        # if in menu, and left mouse is clicked, check if click collides with rect of button
        if game_level == 0:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                if button_start_location.collidepoint(pos):
                    game_level = 1
                if button_exit_location.collidepoint(pos):
                    running = False
        # if screen size changes
        if event.type == pg.VIDEORESIZE:
            # new char and enemy size
            char.update_img_rect(screen.get_height(), char_size)
            for enemy in enemy_group:
                enemy.update_img_rect(screen.get_height(), flyman_size)
            # update start/exit button
            start_button.update_object_rect(screen.get_height(), screen.get_width(), start_button_size, 2)
            exit_button.update_object_rect(screen.get_height(), screen.get_width(), exit_button_size, 1.2)
            # set background image size
            if screen.get_height() * 2.66 < screen.get_width():
                background_menu_img = pg.transform.scale(background_menu_img, (
                    screen.get_width(), screen.get_width() / 2.66)).convert_alpha()
            else:
                background_menu_img = pg.transform.scale(background_menu_img, (
                    screen.get_height() * 2.66, screen.get_height())).convert_alpha()

    # death
    if game_level == "dead":
        screen.blit(deathscreen_img, (0, 0))

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
        # spawn enemies
        if len(enemy_group.sprites()) < 5:
            new_enemy = EnemyFlyman()
            new_enemy.update_img_rect(screen.get_height(), flyman_size)
            enemy_group.add(new_enemy)
        # enemy movement and collision
        for enemy in enemy_group:
            enemy.chase(char)
            if not pg.sprite.collide_rect(char, enemy) is None:
                if not pg.sprite.collide_mask(char, enemy) is None:
                    # game_level = "dead"
                    pass
        # bullet movement and collision
        for bullet in bullet1_group:
            bullet.move()

        # character functions
        char.check_out_of_bounds(ingame_screen.get_width(), ingame_screen.get_height(), stats_screen.get_height())
        char.check_direction()
        char.move_rect()

        # blit everything
        bullet1_group.draw(ingame_screen)
        enemy_group.draw(ingame_screen)
        ingame_screen.blit(char.image, char.rect)
        screen.blit(ingame_screen, (0, screen.get_height() / 8))
        screen.blit(stats_screen, (0, 0))

    # update screen
    pg.display.update()
