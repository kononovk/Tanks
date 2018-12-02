# ----------------------------------------------------
# Program by Nickolay Kononov
#
# Version: 2.0
# Last Update: 29.11.2018
# File: main.py
# File Description: Main program file
# ----------------------------------------------------
import pygame
from player import player as plr
from menu import Menu, killed

"# Data variables #"
window_width = 900
window_height = 700

"# Window creating  #"
pygame.display.set_icon(pygame.image.load(r"textures\icon.png"))
pygame.init()
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("NK_Shooting")
screen = pygame.Surface((window_width, window_height))

"# Font creating #"
pygame.font.init()
hp_font = pygame.font.Font(r"textures\Fonts.ttf", 24)

"# Menu paragraphs #"
par = [(310, 140, u'1 Player', (250, 250, 30), (250, 30, 250), 0),
       (310, 210, u'2 Players', (250, 250, 30), (250, 30, 250), 1),
       (310, 280, u'Exit', (250, 250, 30), (250, 30, 250), 2)]

game = Menu(par)
game_flag = game.menu(screen, win)
screen.fill((0, 0, 0))
"# Information string #"
info_string = pygame.Surface((window_width, 30))

"#______________________________   MAIN   LOOP      ____________________________________#"
"<-------------------------------------------------------------------------------------->"

"# Creating player object #"
tank_list = [r'textures\tanks\tank_up.png', r'textures\tanks\tank_right.png',
             r'textures\tanks\tank_down.png', r'textures\tanks\tank_left.png']
player1 = plr.Player(tank_list, 1, 100, 100)
player1_bullets = []


"---# The beginning of rendering cycle with 2 players #---"
run = True
if game_flag == 2:
    player2 = plr.Player(tank_list, 1, window_width - 100 - 50, window_height - 100 - 50)
    player2_bullets = []
    while run:
        screen.fill((0, 0, 0))
        "# Objects rendering #"
        player1.draw(win)
        player2.draw(win)
        pygame.display.update()
        win.blit(info_string, (0, 0))
        win.blit(screen, (0, 30))
        info_string.fill((25, 80, 40))

        "# Fonts rendering #"
        info_string.blit(hp_font.render(u"(PL1) Lives: " + str(player1.hp), 1, (255, 0, 0)), (10, 5))
        info_string.blit(hp_font.render(u"(PL2) Lives: " + str(player2.hp), 1, (255, 0, 0)), (window_width - 250, 5))

        "# event loop #"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        "# Bullets processing player1 #"
        for bullet in player1_bullets:
            if bullet.x in range(0, window_width + 1):
                bullet.x += bullet.speed_x
            else:
                player1_bullets.pop(player1_bullets.index(bullet))
            if bullet.y in range(0, window_width + 1):
                bullet.y += bullet.speed_y
            else:
                player1_bullets.pop(player1_bullets.index(bullet))
            if bullet.is_hit(player2):
                player1_bullets.pop(player1_bullets.index(bullet))
                player2.hp -= 1


        "# Bullets processing player2 #"
        for bullet in player2_bullets:
            if bullet.x in range(0, window_width + 1):
                bullet.x += bullet.speed_x
            else:
                player2_bullets.pop(player2_bullets.index(bullet))
            if bullet.y in range(0, window_width + 1):
                bullet.y += bullet.speed_y
            else:
                player2_bullets.pop(player2_bullets.index(bullet))
            if bullet.is_hit(player1):
                player2_bullets.pop(player2_bullets.index(bullet))
                player1.hp -= 1

        "# Keys processing #"
        keys = pygame.key.get_pressed()
        player1.update(keys, window_width, window_height, player2, 0)
        player2.update(keys, window_width, window_height, player1, 1)
        if keys[pygame.K_ESCAPE]:
            game.menu(screen, win)

        "# Shooting processing #"
        if keys[pygame.K_SPACE]:
            if len(player1_bullets) < 1:
                player1_bullets.append(plr.Bullet(player1))
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if len(player2_bullets) < 1:
                player2_bullets.append(plr.Bullet(player2))
        for bullet in player1_bullets:
            bullet.draw(win)
        for bullet in player2_bullets:
            bullet.draw(win)

        tmp = killed(player1, player2, screen, win)
        if tmp:
            screen.fill((0, 0, 0))
            player1.hp = 3
            player2.hp = 3
            player1.x, player1.y = 100, 100
            player2.x, player2.y = window_width - 150, window_height - 150
            if tmp == 2:
                game.menu(screen, win)

if game_flag == 1:
    exit()

pygame.font.quit()
pygame.quit()
