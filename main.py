import pygame as pg
import mysql.connector

from character import Character
from enemy import EnemyFlyman
from objects import Object

# connect to db
db_connection_failed = False
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gaming_db"
    )
except mysql.connector.errors.Error:
    db_connection_failed = True


# create full screen surface
screen = pg.display.set_mode((1200, 800))
# set title, icon
pg.display.set_caption("GamingHard")
icon = pg.image.load(r"src/img/logo.png")
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
char = Character(standard_pos_x, standard_pos_y, False)
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

# create energy sprites
energy_size = 50
energy_group = pg.sprite.Group()
energy_full_list = []
for energy in range(0, 5):
    energy_full_list.append(Object(r"src/img/energy.png",
                         stats_screen.get_width() / 2, stats_screen.get_height() / 2, energy_size, energy_size))
energy_empty_list = []
for energy in range(0, 5):
    energy_empty_list.append(Object(r"src/img/energy_empty.png",
                        stats_screen.get_width() / 2, stats_screen.get_height() / 2, energy_size, energy_size))

# enemies
flyman_size = 0.15
enemy_group = pg.sprite.Group()


def upload_score(conn, username):
    try:
        mycursor = conn.cursor()

        # select user from db
        sql = "SELECT Username, High_Score FROM user WHERE Username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()

        # if user already exists, check if new high score
        if len(myresult) > 0:
            for score in myresult:
                if int(score[1]) < char.score:
                    char.new_high_score = True
                    sql = "UPDATE user SET High_Score = %s WHERE Username = %s"
                    val = (char.score, username)
                    mycursor.execute(sql, val)
                    conn.commit()
        # if user doesnt exist, create new user
        else:
            sql = "INSERT INTO user (Username, High_score) VALUES (%s, %s)"
            val = (username, char.score)
            mycursor.execute(sql, val)
            conn.commit()
        return False
    except mysql.connector.errors.Error:
        return True


new_high_score = False

pg.init()

# game loop
running = True
clock = pg.time.Clock()

while running:

    # FPS = 30
    clock.tick(30)

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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                    # TODO: add username input
                    if db_connection_failed is False:
                        db_connection_failed = upload_score(conn, username="test")
                    enemy_group.empty()
                    bullet1_group.empty()
                    if char.new_high_score is True:
                        new_high_score = True
                    char = Character(standard_pos_x, standard_pos_y, False)
                    char.update_img_rect(screen.get_height(), char_size)
                    char.score = 0
                    game_level = 0
        if game_level == 1:
            # character move, shoot bullet
            char.change_speed(event)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if char.energy > 0:
                    pos = pg.mouse.get_pos()
                    bullet1_group.add(char.create_bullet1(pos, stats_screen.get_height()))
            for bullet in bullet1_group:
                bullet.check_out_of_bounds(bullet1_group, ingame_screen.get_rect())
        # if in menu, and left mouse is clicked, check if click collides with rect of button
        if game_level == 0:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                if button_start_location.collidepoint(pos):
                    game_level = 1
                    new_high_score = False
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

    # death screen
    if game_level == "dead":
        img_rect = deathscreen_img.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(deathscreen_img, img_rect)
        font = pg.font.SysFont('Comic Sans MS', 30)
        # deathscreen text
        deathscreen_text = font.render('Press "SPACE" to continue and save your score.', False, (255, 255, 255))
        deathsreen_text_rect = deathscreen_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 1.1))
        screen.blit(deathscreen_text, deathsreen_text_rect)
        # deathscreen score
        deathscreen_score = font.render('Score: ' + str(char.score), False, (255, 255, 255))
        deathsreen_score_rect = deathscreen_score.get_rect(center=(screen.get_width() / 2, screen.get_height() / 1.2))
        screen.blit(deathscreen_score, deathsreen_score_rect)

    # menu
    if game_level == 0:
        # blit menu elements
        menu_screen.blit(background_menu_img, (0, 0))
        start_button.move_rect()
        button_start_location = menu_screen.blit(start_button.image, start_button.rect)
        exit_button.move_rect()
        button_exit_location = menu_screen.blit(exit_button.image, exit_button.rect)
        # if database connection failed
        if db_connection_failed is True:
            font = pg.font.SysFont('Comic Sans MS', 30)
            failed_conn_text = font.render('Error: Connection to Database failed', False, (0, 0, 0))
            failed_conn_text_rect = failed_conn_text.get_rect(
                center=(screen.get_width() / 2, screen.get_height() / 1.1))
            menu_screen.blit(failed_conn_text, failed_conn_text_rect)
        # if new high score
        if new_high_score is True:
            font = pg.font.SysFont('Comic Sans MS', 36)
            high_score_text = font.render('You have got a new high score!', False, (0, 0, 0))
            high_score_text_rect = high_score_text.get_rect(
                center=(screen.get_width() / 2, screen.get_height() / 1.7))
            menu_screen.blit(high_score_text, high_score_text_rect)
        screen.blit(menu_screen, (0, 0))

    # TODO: normalize enemy movement
    # TODO: add stats(max score)
    # ingame lvl 1
    if game_level == 1:
        char.update_energy()
        char.update_energy_img(energy_group, energy_full_list, energy_empty_list, stats_screen)
        # bullet movement and collision
        for bullet in bullet1_group:
            bullet.move()
            death_count_prior = bullet.death_count
            bullet.check_collision(enemy_group)
            for deaths in range(death_count_prior, bullet.death_count):
                char.score += 100 * (deaths + 1)
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
                    game_level = "dead"

        # character functions
        char.check_out_of_bounds(ingame_screen.get_width(), ingame_screen.get_height(), stats_screen.get_height())
        char.check_direction()
        char.move_rect()

        # blit score
        font = pg.font.SysFont('Comic Sans MS', 32)
        score_text = font.render("Score: " + str(char.score), False, (0, 0, 0))
        score_text_rect = score_text.get_rect(center=(stats_screen.get_width() / 5, stats_screen.get_height() / 2))
        stats_screen.blit(score_text, score_text_rect)
        # blit bullets
        bullet1_group.draw(ingame_screen)
        # blit enemies
        for enemy in enemy_group:
            if enemy.hit_status <= 0:
                ingame_screen.blit(enemy.image, enemy.rect)
            else:
                ingame_screen.blit(enemy.image_hit, enemy.rect)
                enemy.hit_status -= 1
        # blit screens
        ingame_screen.blit(char.image, char.rect)
        screen.blit(ingame_screen, (0, screen.get_height() / 8))
        energy_group.draw(stats_screen)
        screen.blit(stats_screen, (0, 0))

    # update screen
    pg.display.update()
