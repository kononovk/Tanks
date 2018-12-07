import pygame

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 60
PLATFORM_COLOR = "#FF6262"


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'textures\block.png')
        self.image.blit(self.image, (0, 0), (x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.x = x
        self.y = y
