# ----------------------------------------------------
# Program by Kirill Obuhov
#
# Version: 1.0
# Last Update: 02.12.2018
# File: menu.py
# File Description: Main menu program file
# ----------------------------------------------------
import pygame
from player.player import Player, Bullet
from bot.bot import Bot, BulletBot

tank_list = [r'textures\tanks\tank_up.png', r'textures\tanks\tank_right.png',
             r'textures\tanks\tank_down.png', r'textures\tanks\tank_left.png']

# Main menu class
class Menu:
    def __init__(self, paragraphs):
        self.paragraphs = paragraphs

    def render(self, host, font, num_par):
        for i in self.paragraphs:
            if num_par == i[5]:
                host.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))
            else:
                host.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))

    "# Menu starting function#"
    def menu(self, screen, win, menu_color=(0, 100, 200)):
        done = True
        font_menu = pygame.font.Font(r"textures\Fonts.ttf", 50)
        prg = 0
        while done:
            screen.fill(menu_color)
            mp = pygame.mouse.get_pos()
            for i in self.paragraphs:
                if (mp[0] > i[0]) and (mp[0] < i[0]+155) and (mp[1] > i[1]) and (mp[1] < i[1]+150):
                    prg = i[5]
            self.render(screen, font_menu, prg)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        exit()
                    if e.key == pygame.K_UP and prg > 0:
                        prg -= 1
                    if e.key == pygame.K_DOWN and prg < len(self.paragraphs) - 1:
                        prg += 1
                    if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                        if prg == 0:
                            return 1
                        elif prg == 1:
                            return 2
                        elif prg == 2:
                            exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if prg == 0:
                        return 1
                    elif prg == 1:
                        return 2
                    elif prg == 2:
                        exit()
            win.blit(screen, [0, 0])
            pygame.display.flip()


def killed(player1, player2, screen, win):
    if player1.is_killed() or player2.is_killed():
        par = [(310, 140, u'Try again', (250, 250, 30), (250, 30, 250), 0),
               (310, 210, u'Main Menu', (250, 250, 30), (250, 30, 250), 1),
               (310, 280, u'Exit', (250, 250, 30), (250, 30, 250), 2)]
        end_menu = Menu(par)
        game_flag = end_menu.menu(screen, win, (0, 0, 0))
        # If user have chosen 'try again' return 1
        if game_flag == 1:
            return 1
        # If user have chosen 'Main Menu' return 2
        if game_flag == 2:
            return 2
    return False

def killed_player(player1, screen, win):
    if player1.is_killed():
        par = [(310, 140, u'Try again', (250, 250, 30), (250, 30, 250), 0),
               (310, 210, u'Main Menu', (250, 250, 30), (250, 30, 250), 1),
               (310, 280, u'Exit', (250, 250, 30), (250, 30, 250), 2)]
        end_menu = Menu(par)
        game_flag = end_menu.menu(screen, win, (0, 0, 0))
        # If user have chosen 'try again' return 1
        if game_flag == 1:
            return 1
        # If user have chosen 'Main Menu' return 2
        if game_flag == 2:
            return 2
    return False

def killed_bot(addbot):
    for i in range(0,len(addbot)):
        if addbot[i].is_killed():
            addbot.pop(i)
            addbot.append(Bot(tank_list, 1))
            addbot.append(Bot(tank_list, 1))
    return addbot

