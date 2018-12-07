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
from menu import Menu, killed, killed_player

def killed_bot(addbot, player):
    for i in range(0,len(addbot)):
        if addbot[i].is_killed(player):
            addbot.pop(i)
            bot_bullets.pop(i)
            bot_bullets.append([])
            bot_bullets.append([])
            addbot.append(boobs.Bot(tank_list2, noblock_x, noblock_y, player1, 0.4))
            addbot.append(boobs.Bot(tank_list2, noblock_x, noblock_y, player1, 0.4))
    return addbot

def hp_render(player1, player2):
    pass

"# Data variables #"
window_width = 900
window_height = 660

"# Window creating  #"
pygame.display.set_icon(pygame.image.load(r"textures\icon.png"))
pygame.init()
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("NKOK_Shooting")
screen = pygame.Surface((window_width, window_height))

"# Font creating #"
pygame.font.init()
hp_font = pygame.font.Font(r"textures\Fonts.ttf", 24)

"# Menu paragraphs #"
par = [(310, 280, u'1 Player', (250, 250, 30), (250, 250, 250), 0),  # purple = (250, 30, 250)
       (310, 350, u'2 Players', (250, 250, 30), (250, 250, 250), 1),
       (310, 420, u'Exit', (250, 250, 30), (250, 250, 250), 2)]

game = Menu(par)
game_flag = game.menu(screen, win)
screen.fill((0, 0, 0))

"# Information string #"
info_string = pygame.Surface((window_width, 30))

"#______________________________   MAIN   LOOP      ____________________________________#"
"<-------------------------------------------------------------------------------------->"

"# Creating player object #"
tank_list = [r'textures\tanks\tank_'
             r'up.png', r'textures\tanks\tank_right.png',
             r'textures\tanks\tank_down.png', r'textures\tanks\tank_left.png']
tank_list2 = [r'textures\tanks\tank2_up.png', r'textures\tanks\tank2_right.png',
             r'textures\tanks\tank2_down.png', r'textures\tanks\tank2_left.png']
player1 = plr.Player(tank_list, 1, 1, 100, 100)
player1_bullets = []

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 60
PLATFORM_COLOR = "#FF6262"

"# Lifes textures images #"
life1_img = pygame.image.load(r'textures\life1.png')
life2_img = pygame.image.load((r'textures\life2.png'))

"---# The beginning of rendering cycle with 2 players #---"
run, run_main = True, True

while run_main:
    "# List with life's rendering coordinates #"
    life1_rect = [pygame.Rect((0, 0), (0, 0)),
                  pygame.Rect((30, 0), (0, 0)),
                  pygame.Rect((60, 0), (0, 0))]  # coordinates, (width, height)
    life2_rect = [pygame.Rect((window_width - 30, 0), (0, 0)),
                  pygame.Rect((window_width - 60, 0), (0, 0)),
                  pygame.Rect((window_width - 90, 0), (0, 0))]

    run = True
    if game_flag == 1:
        addbot = []
        bot_bullets = []
        bot_bullets.append([])
        entities = pygame.sprite.Group()        # all objects
        platforms = []                          # blocks, we will bump on
        entities.add(player1)
        noblock_x = []
        noblock_y = []
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
        for i in range(0,len(level)):                       # all string
            for j in range(0, len(level[i])):                     # each symbol
                if level[i][j] == "-":
                    pf = plt.Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)
                else:
                    noblock_x.append(j)
                    noblock_y.append(i)
                x += PLATFORM_WIDTH             # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT                # то же самое и с высотой
            x = 0
        addbot.append(boobs.Bot(tank_list2, noblock_x, noblock_y, player1,0.4))
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
                if bullet.y in range(0, window_height + 1):
                    bullet.y += bullet.speed_y
                else:
                    player1_bullets.pop(player1_bullets.index(bullet))
                for p in platforms:
                    if (bullet.x <= p.x + 60 and bullet.x >= p.x) and (bullet.y <= p.y + 60 and bullet.y >= p.y) and len(player1_bullets) != 0:
                        player1_bullets.pop(player1_bullets.index(bullet))
                for bot in addbot:
                    if bullet.is_hit(bot) and len(player1_bullets) != 0:
                        player1_bullets.pop(player1_bullets.index(bullet))
                        bot.hp -= 1

            "# Bullets processing bot #"
            for i in range(0, len(addbot)):
                for bullet in bot_bullets[i]:
                    if bullet.x in range(0, window_width + 1):
                        bullet.x += bullet.speed_x
                    elif len(bot_bullets[i]) != 0:
                        bot_bullets[i].pop(bot_bullets[i].index(bullet))
                    if bullet.y in range(0, window_height + 1):
                        bullet.y += bullet.speed_y
                    elif len(bot_bullets[i]) != 0:
                        bot_bullets[i].pop(bot_bullets[i].index(bullet))
                    for p in platforms:
                        if (bullet.x <= p.x + 60 and bullet.x >= p.x) and \
                           (bullet.y <= p.y + 60 and bullet.y >= p.y) and \
                           (len(bot_bullets[i]) != 0):
                            bot_bullets[i].pop(bot_bullets[i].index(bullet))
                    if bullet.is_hit_bot(player1) and len(bot_bullets[i]) != 0:
                        bot_bullets[i].pop(bot_bullets[i].index(bullet))
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
                if ((addbot[i].x >= player1.x and addbot[i].x <= player1.x + 60) or
                    (addbot[i].y >= player1.y  and addbot[i].y <= player1.y + 60)) and len(bot_bullets[i]) < 1:
                    bot_bullets[i].append(boobs.BulletBot(addbot[i]))

            "# Bullets drawing #"
            for i in range(0, len(bot_bullets)):
                for bullet in bot_bullets[i]:
                    bullet.draw(win)

            for bullet in player1_bullets:
                bullet.draw(win)

            "# Kills checking #"
            addbot = killed_bot(addbot, player1)
            tmp = killed_player(player1, screen, win)
            if tmp:
                screen.fill((0, 0, 0))
                player1.hp = 1000
                player1.x, player1.y = 100, 100
                player1_bullets.clear()
                bot_bullets.clear()
                if tmp == 2:
                    game_flag = game.menu(screen, win)
                run = False

    if game_flag == 2:
        player2 = plr.Player(tank_list2, 1, 2, window_width - 100 - 50, window_height - 100 - 50)
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

            "# Lifes rendering #"
            for i in life1_rect:
                win.blit(life1_img, i)
            for i in life2_rect:
                win.blit(life2_img, i)
            # info_string.blit(hp_font.render(u"(PL1) Lives: " + str(player1.hp), 1, (255, 0, 0)), (10, 5))
            # info_string.blit(hp_font.render(u"(PL2) Lives: " + str(player2.hp), 1, (255, 0, 0)), (window_width - 250, 5))

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
                    if len(player1_bullets) != 0:
                        player1_bullets.pop(player1_bullets.index(bullet))
                    if len(life2_rect) != 0:
                        life2_rect.pop(player2.hp)


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
                    if len(life1_rect) != 0:
                        life1_rect.pop(2 - player1.hp)

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
                player1_bullets.clear()
                player2_bullets.clear()
                if tmp == 2:
                    game_flag = game.menu(screen, win)
                    run = False
                if tmp == 1:
                    life1_rect = [pygame.Rect((0, 0), (0, 0)),
                                  pygame.Rect((30, 0), (0, 0)),
                                  pygame.Rect((60, 0), (0, 0))]  # coordinates, (width, height)
                    life2_rect = [pygame.Rect((window_width - 30, 0), (0, 0)),
                                  pygame.Rect((window_width - 60, 0), (0, 0)),
                                  pygame.Rect((window_width - 90, 0), (0, 0))]

pygame.font.quit()
pygame.quit()
