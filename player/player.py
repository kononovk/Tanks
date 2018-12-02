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
ZOMBIE_GREEN = (122, 172, 34)
(DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)


class Player(pygame.sprite.Sprite):
    speed = 5
    width = 60
    height = 60
    x = 0
    y = 0
    hp = 3
    x_center = x + width/2
    y_center = y + height / 2

    def __init__(self, list_file_name, speed=2, x=0, y=0, direction=randint(0, 3)):
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
        ''' self.image.get_rect(center=(x + self.width/2, y + self.height / 2)) '''

        self.speed = speed
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(self.image, self.rect)

    def update(self, keys, window_width, window_height, pl, num=0):
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
            elif (keys[pygame.K_w] or keys[pygame.K_w]) and self.y > 30:
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
        self.collide(pl)

    def collide(self, player2):
        if pygame.sprite.collide_rect(self, player2):
            if self.direction == self.prev_direction:
                self.speed = 0
            else:
                self.prev_direction = self.direction
                self.speed = 1
        else:
            self.speed = 1


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
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)