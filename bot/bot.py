import pygame
from random import randint

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 119, 0)
(DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)


class Bot(pygame.sprite.Sprite):
    width = 60
    height = 60
    hp = 2

    def __init__(self, list_file_name, speed=1, direction=randint(0, 3)):
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

        self.x = randint(60, 900 - 60)
        self.y = randint(60, 700 - 60)
        self.x_center = self.x + self.width / 2
        self.y_center = self.y + self.height / 2

    def draw(self, win):
        win.blit(self.image, self.rect)

    def update(self, window_width, window_height, pl, platforms):
        self.direction = randint(0, 3)
        if self.direction == DIR_LEFT:
            if self.x > 0 and self.rect.collidelist(platforms) == -1:
                self.prev_direction = self.direction
                self.image = self.image_left
                self.direction = DIR_LEFT
                self.x -= self.speed
        if self.direction == DIR_RIGHT:
            if self.x < window_width - self.width and self.rect.collidelist(platforms) != -1:
                self.prev_direction = self.direction
                self.image = self.image_right
                self.direction = DIR_RIGHT
                self.x += self.speed
        if self.direction == DIR_DOWN:
            if self.y < window_height - self.height and self.rect.collidelist(platforms) != -1:
                self.prev_direction = self.direction
                self.image = self.image_down
                self.direction = DIR_DOWN
                self.y += self.speed
        if self.direction == DIR_UP:
            if self.y > 30 and self.rect.collidelist(platforms) != -1:
                self.prev_direction = self.direction
                self.image = self.image_up
                self.direction = DIR_UP
                self.y -= self.speed
        self.x_center = self.x + self.width / 2
        self.y_center = self.y + self.height / 2
        self.rect = self.surface.get_rect(center=(self.x_center, self.y_center))
        self.collide(pl, platforms)

    def collide(self, player1, platforms):
        # Collides with another player processing #
        if pygame.sprite.collide_rect(self, player1):
            if self.direction == self.prev_direction:
                self.speed = 0
                if self.direction == DIR_RIGHT:
                    self.x = player1.x - player1.width
                if self.direction == DIR_LEFT:
                    self.x = player1.x + player1.width
                if self.direction == DIR_UP:
                    self.y = player1.y + player1.height
                if self.direction == DIR_DOWN:
                    self.y = player1.y - player1.height
            else:
                self.speed = 1
                self.prev_direction = self.direction
        else:
            self.speed = 1

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


def set_coord(bot):
    if bot.direction == DIR_UP:
        x = int(bot.x_center)
        y = bot.y
    elif bot.direction == DIR_RIGHT:
        x = bot.x + bot.width
        y = int(bot.y + bot.height / 2)
    elif bot.direction == DIR_LEFT:
        x = bot.x
        y = int(bot.y + bot.height / 2)
    else:
        x = int(bot.x + bot.width / 2)
        y = bot.y + bot.height
    return [x, y]


class BulletBot(pygame.sprite.Sprite):
    def __init__(self, bot, radius=4, color=WHITE):
        pygame.sprite.Sprite.__init__(self)
        self.x = set_coord(bot)[0]
        self.y = set_coord(bot)[1]

        # Image #
        self.image = pygame.Surface([8, 8])
        self.rect = self.image.get_rect()
        self.color = color
        self.direction = bot.direction
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

    def is_hit_bot(self, bot):
        flag_x = (self.x > bot.x) and (self.x < bot.x + bot.width)
        flag_y = (self.y > bot.y) and (self.y < bot.y + bot.height)
        if flag_x and flag_y:
            return True
        return False
