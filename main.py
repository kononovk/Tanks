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
from bot import bot as boobs
from block import block as plt
from menu import Menu, killed_bot, killed, killed_player

"# Data variables #"
window_width = 900
window_height = 660

"# Window creating  #"
pygame.display.set_icon(pygame.image.load(r"textures\icon.png"))
pygame.init()
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("nKOK_Shooting")
screen = pygame.Surface((window_width, window_height))

"# Font creating #"
pygame.font.init()
hp_font = pygame.font.Font(r"textures\Fonts.ttf", 24)

"# Menu paragraphs #"
par = [(310, 280, u'1 Player', (250, 250, 30), (250, 250, 250), 0),  # purple = (250, 30, 250)
       (310, 350, u'2 Players', (250, 250, 30), (250, 250, 250), 1), #
       (310, 420, u'Exit', (250, 250, 30), (250, 250, 250), 2)]      #

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
player1 = plr.Player(tank_list, 1, 100, 100, 1)
player1_bullets = []

timer = pygame.time.Clock()

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 60
PLATFORM_COLOR = "#FF6262"


"---# The beginning of rendering cycle with 2 players #---"
run, run_main = True, True

while run_main:
    run = True
    if game_flag == 1:
        addbot = []
        addbot.append(boobs.Bot(tank_list, 1))
        bot_bullets = []
        entities = pygame.sprite.Group()        # all objects
        platforms = []                          # blocks, we will bump on
        entities.add(player1)
        noblock = []
        level = ['---------------',
                 '-   -     -   -',
                 '-   -     -   -',
                 '-   -         -',
                 '-   -         -',
                 '-   -     -   -',
                 '-   -     -   -',
                 '-   -     -   -',
                 '-         -   -',
                 '-         -   -',
                 '---------------']
        x = y = 0                               # coordinates
        for row in level:                       # all string
            for col in row:                     # each symbol
                if col == "-":
                    pf = plt.Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)
                x += PLATFORM_WIDTH             # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT                # то же самое и с высотой
            x = 0
        while run:
            screen.fill((0, 0, 0))
            "# Objects rendering #"
            for i in range(0, len(addbot)):
                addbot[i].draw(win)
            entities.draw(win)
            pygame.display.update()
            win.blit(info_string, (0, 0))
            win.blit(screen, (0, 30))
            info_string.fill((25, 80, 40))

            "# Fonts rendering #"
            info_string.blit(
                hp_font.render(u"(PL1) Lives: " + str(player1.hp), 1, (255, 0, 0)),
                (10, 5))
            "# event loop #"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

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
                for p in platforms:
                    if (bullet.x <= p.x + 60 and bullet.x >= p.x) and (bullet.y <= p.y + 60 and bullet.y >= p.y):
                        player1_bullets.pop(player1_bullets.index(bullet))
                for bot in addbot:
                    if bullet.is_hit(bot) and len(player1_bullets) != 0:
                        player1_bullets.pop(player1_bullets.index(bullet))
                        bot.hp -= 1

            "# Bullets processing bot #"
            for bullet in bot_bullets:
                if bullet.x in range(0, window_width + 1):
                    bullet.x += bullet.speed_x
                else:
                    bot_bullets.pop(bot_bullets.index(bullet))
                if bullet.y in range(0, window_width + 1):
                    bullet.y += bullet.speed_y
                else:
                    bot_bullets.pop(bot_bullets.index(bullet))
                for p in platforms:
                    if (bullet.x <= p.x + 60 and bullet.x >= p.x) and (bullet.y <= p.y + 60 and bullet.y >= p.y):
                        bot_bullets.pop(bot_bullets.index(bullet))
                if bullet.is_hit_bot(player1):
                    bot_bullets.pop(bot_bullets.index(bullet))
                    player1.hp -= 1

            keys = pygame.key.get_pressed()
            player1.update(keys, window_width, window_height, addbot[0], platforms, 0)

            for bot in addbot:
                bot.update(window_width, window_height, player1, platforms)

            "# Keys processing #"
            if keys[pygame.K_ESCAPE]:                              # Exit yo menu
                tmp = game.menu(screen, win)
                if game_flag != tmp:
                    player1.x = 100
                    player1.y = 100
                    game_flag  = tmp
                run = False
            elif keys[pygame.K_SPACE]:                             # Player's bullets
                if len(player1_bullets) < 1:
                    player1_bullets.append(plr.Bullet(player1))

            "# Bot's bullets #"
            for i in range(0, len(addbot)):
                if addbot[i].x == player1.x or addbot[i].y == player1.y:
                    addbot[i].speed = 0
                    bot_bullets.append(boobs.BulletBot(bot))

            "# Bullets drawing #"
            for bullet in bot_bullets:
                bullet.draw(win)

            for bullet in player1_bullets:
                bullet.draw(win)

            "# Kills checking #"
            addbot = killed_bot(addbot)
            tmp = killed_player(player1, screen, win)
            if tmp:
                screen.fill((0, 0, 0))
                player1.hp = 3
                player1.x, player1.y = 100, 100
                if tmp == 2:
                    game_flag = game.menu(screen, win)
                run = False

    if game_flag == 2:
        player2 = plr.Player(tank_list, 1, window_width - 100 - 50, window_height - 100 - 50, 2)
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
                    exit()

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
                    player2.hp -= 1
                    if len(player2_bullets) != 0:
                        player1_bullets.pop(player1_bullets.index(bullet))


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
                    player1.hp -= 1
                    if len(player2_bullets) != 0:
                        player2_bullets.pop(player2_bullets.index(bullet))

            "# Keys processing #"
            keys = pygame.key.get_pressed()
            player1.update(keys, window_width, window_height, player2, None, 0)
            player2.update(keys, window_width, window_height, player1, None, 1)
            if keys[pygame.K_ESCAPE]:
                tmp = game.menu(screen, win)
                if game_flag != tmp:
                    player1.x = 100
                    player1.y = 100
                    game_flag  = tmp
                run = False

            "# Shooting processing #"
            if keys[pygame.K_SPACE]:
                if len(player1_bullets) < 1:
                    player1_bullets.append(plr.Bullet(player1))
            if keys[pygame.K_KP_ENTER]:
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
                    game_flag = game.menu(screen, win)
                    run = False


pygame.font.quit()
pygame.quit()
