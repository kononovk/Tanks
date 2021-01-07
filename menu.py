# ----------------------------------------------------
# Program by Kirill Obuhov
#
# Version: 1.2
# Last Update: 02.12.2018
# File: menu.py
# File Description: Main menu program file
# ----------------------------------------------------
import pygame
from player.player import Player, Bullet
from bot.bot import Bot, BulletBot


tank_list2 = [r'textures/tanks/tank2_up.png', r'textures/tanks/tank2_right.png',
              r'textures/tanks/tank2_down.png', r'textures/tanks/tank2_left.png']


# Main menu class
class Menu(pygame.sprite.Sprite):
    def __init__(self, paragraphs, FName = r'./textures/battle-city.png', x = 125, y = 10, wins=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(FName)
        self.rect = pygame.Rect(x, y, 100, 100)
        self.x = x
        self.y = y
        self.paragraphs = paragraphs
        self.wins = wins

    def render(self, host, font, num_par, flag=0):
        for i in self.paragraphs:
            if num_par == i[5]:
                host.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))
            else:
                host.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            host.blit(self.image, self.rect)
            if flag != 0:
                host.blit(font.render(u"Wins player " + str(flag), 1, (255, 215, 0)), (265, 500))

    "# Menu starting function#"
    def menu(self, screen, win, menu_color=(0, 0, 0)): # 0, 100, 200
        done = True
        font_menu = pygame.font.Font(r"./textures/Fonts.ttf", 50)
        prg = 0
        while done:
            screen.fill(menu_color)
            mp = pygame.mouse.get_pos()
            for i in self.paragraphs:
                if (mp[0] > i[0]) and (mp[0] < i[0]+155) and (mp[1] > i[1]) and (mp[1] < i[1]+150):
                    prg = i[5]
            self.render(screen, font_menu, prg, self.wins)

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
                    if e.key == pygame.K_RETURN:
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
    pl1 = player1.is_killed()
    pl2 = player2.is_killed()
    if pl1 or pl2:
        par = [(310, 280, u'Try again', (250, 250, 30), (250, 250, 250), 0),
               (310, 350, u'Main Menu', (250, 250, 30), (250, 250, 250), 1),
               (310, 420, u'Exit', (250, 250, 30), (250, 250, 250), 2)]
        if pl1:
            end_menu = Menu(par, r'textures/game-over.png', 260, 70, 2)
        else:
            end_menu = Menu(par, r'textures/game-over.png', 260, 70, 1)
        game_flag = end_menu.menu(screen, win, (0, 0, 0))
        # If user have chosen 'try again' return 1
        if game_flag == 1:
            return 1
        # If user have chosen 'Main Menu' return 2
        if game_flag == 2:
            return 2
    return False

def killed_player(player1, screen, win, last_rec):
    if player1.is_killed():
        "# Writing new record in file #"
        if player1.points > int(last_rec):
            last_rec = player1.points
        f = open("record.txt", 'w')
        f.write(str(last_rec))
        player1.points = 0
        f.close()

        par = [(310, 280, u'Try again', (250, 250, 30), (250, 250, 250), 0),
               (310, 350, u'Main Menu', (250, 250, 30), (250, 250, 250), 1),
               (310, 420, u'Exit', (250, 250, 30), (250, 250, 250), 2)]
        end_menu = Menu(par, r'textures/game-over.png', 260, 70)
        game_flag = end_menu.menu(screen, win, (0, 0, 0))
        # If user have chosen 'try again' return 1
        if game_flag == 1:
            return 1
        # If user have chosen 'Main Menu' return 2
        if game_flag == 2:
            return 2
    return False



