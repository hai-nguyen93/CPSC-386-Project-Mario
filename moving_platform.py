import pygame
from pygame.sprite import Sprite


class MovingPlatform(Sprite):
    def __init__(self, screen, tag, left, bottom, direction, mode, x_range=None, y_range=None, size=None):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.tag = tag
        self.mode = mode
        self.x_range = x_range
        self.y_range = y_range
        if size is None:
            self.image = pygame.image.load('images/Tile/moving_platform.png')
        if size == 'small':
            self.image = pygame.image.load('images/Tile/moving_platform_small.png')
        if size == 'med':
            self.image = pygame.image.load('images/Tile/moving_platform_med.png')
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.inital_x = left
        self.inital_y = bottom
        self.rect.bottom = bottom
        self.direction = direction

    def update(self, sprites):
        if self.mode == 'vertical':
            if self.rect.centery > self.screen_rect.bottom:
                self.rect.bottom = 10
            if self.rect.centery < 0:
                self.rect.bottom = self.screen_rect.bottom
            if self.y_range is not None:
                if self.rect.centery > self.y_range + self.inital_y:
                    self.direction = -1
                if self.rect.centery < self.inital_y:
                    self.direction = 1
            self.rect.bottom += self.direction
        if self.mode == 'horizontal':
            if self.x_range is not None:
                if self.rect.centerx > self.inital_x + self.x_range:
                    self.direction = -1
                if self.rect.centerx < self.inital_x:
                    self.direction = 1
                self.rect.x += self.direction

    def draw(self, camera):
        self.screen.blit(self.image, camera.apply(self))
