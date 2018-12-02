# ----------------------------------------------------
# Program by Kirill Obuhov
#
# Version: 1.0
# Last Updatez: 30.11.2018
# File: menu.py
# File Description: Main menu program file
# ----------------------------------------------------
import pygame

"# Menu main class #"
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
    def menu(self, screen, win):
        done = True
        font_menu = pygame.font.Font(r"textures\Fonts.ttf", 50)
        prg = 0
        while done:
            screen.fill((0, 100, 200))
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
