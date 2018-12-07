# ----------------------------------------------------
# Program by Nickolay Kononov
#
# Version: 1.0
# Last Update: 30.09.2018
# File: player.py
# File Description: This file contains player's class
# ----------------------------------------------------
import pygame
from random import randint

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 119, 0)
(DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)

class Player(pygame.sprite.Sprite):
    width = 60
    height = 60
    hp = 1000
    points = 0

    def __init__(self, list_file_name, speed, id, x=0, y=0, direction=randint(0, 3)):
        self.id = id
        pygame.sprite.Sprite.__init__(self)
        # images for different directions
        self.image_up = pygame.image.load(list_file_name[0]).convert_alpha()
        self.image_right = pygame.image.load(list_file_name[1]).convert_alpha()
        self.image_down = pygame.image.load(list_file_name[2]).convert_alpha()
        self.image_left = pygame.image.load(list_file_name[3]).convert_alpha()
        self.direction = direction
        self.prev_direction = direction
        self.image = pygame.image.load(list_file_name[direction]).convert_alpha()

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.blit(self.image, (0, 0), (0, 0, self.width, self.height))
        self.rect = self.surface.get_rect()
        self.speed = speed
        self.x = x
        self.y = y
        self.x_center = self.x + self.width / 2
        self.y_center = self.y + self.height / 2

    def draw(self, win):
        win.blit(self.image, self.rect)

    def update(self, keys, window_width, window_height, pl, platforms, num=0, flag = True):
        if flag:
            if num == 0:
                if keys[pygame.K_a] and self.x > 0:
                    self.prev_direction = self.direction
                    self.image = self.image_left
                    self.direction = DIR_LEFT
                    self.x -= self.speed
                elif keys[pygame.K_d] and self.x < window_width - self.width:
                    self.prev_direction = self.direction
                    self.image = self.image_right
                    self.direction = DIR_RIGHT
                    self.x += self.speed
                elif keys[pygame.K_s] and self.y < window_height - self.height:
                    self.prev_direction = self.direction
                    self.image = self.image_down
                    self.direction = DIR_DOWN
                    self.y += self.speed
                elif keys[pygame.K_w] and self.y > 30:
                    self.prev_direction = self.direction
                    self.image = self.image_up
                    self.direction = DIR_UP
                    self.y -= self.speed
            else:
                if keys[pygame.K_LEFT] and self.x > 0:
                    self.prev_direction = self.direction
                    self.image = self.image_left
                    self.direction = DIR_LEFT
                    self.x -= self.speed
                elif keys[pygame.K_RIGHT] and self.x < window_width - self.width:
                    self.prev_direction = self.direction
                    self.image = self.image_right
                    self.direction = DIR_RIGHT
                    self.x += self.speed
                elif keys[pygame.K_DOWN] and self.y < window_height - self.height:
                    self.prev_direction = self.direction
                    self.image = self.image_down
                    self.direction = DIR_DOWN
                    self.y += self.speed
                elif (keys[pygame.K_UP]) and self.y > 30:
                    self.prev_direction = self.direction
                    self.image = self.image_up
                    self.direction = DIR_UP
                    self.y -= self.speed
            self.x_center = self.x + self.width / 2
            self.y_center = self.y + self.height / 2
            self.rect = self.surface.get_rect(center=(self.x_center, self.y_center))
        self.collide(pl, platforms)

    "# Main collides processing function #"
    def collide(self, player2, platforms):
        "# Collides with another player processing #"
        if pygame.sprite.collide_rect(self, player2):
            flag = False
            for i in range(0, player2.width + 1):
                if player2.rect.collidepoint(self.x + i,self.y) and self.direction == DIR_UP:
                    self.speed = 0
                    flag = True
                elif player2.rect.collidepoint(self.x,self.y + i) and self.direction == DIR_LEFT:
                    self.speed = 0
                    flag = True
                elif player2.rect.collidepoint(self.x + i,self.y + 60) and self.direction == DIR_DOWN:
                    self.speed = 0
                    flag = True
                elif player2.rect.collidepoint(self.x + 60,self.y + i) and self.direction == DIR_RIGHT:
                    self.speed = 0
                    flag = True
            if not flag:
                self.speed = 1
        else:
            self.speed = 1


        "# Collides with platforms processing #"
        if platforms != None:
            if self.rect.collidelist(platforms) != -1:
                if self.direction == self.prev_direction:
                    self.speed = 0
                    if self.direction == DIR_RIGHT:
                        self.x = platforms[self.rect.collidelist(platforms)].x - 60
                    if self.direction == DIR_LEFT:
                        self.x = platforms[self.rect.collidelist(platforms)].x + 60
                    if self.direction == DIR_UP:
                        self.y = platforms[self.rect.collidelist(platforms)].y + 60
                    if self.direction == DIR_DOWN:
                        self.y = platforms[self.rect.collidelist(platforms)].y - 60
                else:
                    self.speed = 1
                    self.prev_direction = self.direction
            else:
                self.speed = 1

    def is_killed(self):
        if self.hp > 0:
            return False
        return True


def set_coord(player):
    if player.direction == DIR_UP:
        x = int(player.x_center)
        y = player.y
    elif player.direction == DIR_RIGHT:
        x = player.x + player.width
        y = int(player.y + player.height / 2)
    elif player.direction == DIR_LEFT:
        x = player.x
        y = int(player.y + player.height / 2)
    else:
        x = int(player.x + player.width / 2)
        y = player.y + player.height
    return [x, y]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pl, radius=4, color=WHITE):
        pygame.sprite.Sprite.__init__(self)
        self.x = set_coord(pl)[0]
        self.y = set_coord(pl)[1]

        # Image #
        self.image = pygame.Surface([8, 8])
        self.rect = self.image.get_rect()
        self.color = color
        self.direction = pl.direction
        self.radius = radius

        # Direction processing #
        if self.direction == DIR_UP:
            self.facing_y = -1
        elif self.direction == DIR_DOWN:
            self.facing_y = 1
        else:
            self.facing_y = 0
        if self.direction == DIR_RIGHT:
            self.facing_x = 1
        elif self.direction == DIR_LEFT:
            self.facing_x = -1
        else:
            self.facing_x = 0
        self.speed_x = 2 * self.facing_x
        self.speed_y = 2 * self.facing_y

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def is_hit(self, player):
        flag_x = self.x > player.x and self.x < player.x + player.width
        flag_y = self.y > player.y and self.y < player.y + player.height
        if flag_x and flag_y:
            return True
        return False



