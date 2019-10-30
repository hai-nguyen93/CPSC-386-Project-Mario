import pygame
from pygame.sprite import Sprite


class WarpZone(Sprite):
    def __init__(self, tag, id, left, bot):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.left = left
        self.rect.bottom = bot
        self.tag = tag
        self.id = id

    def draw(self, screen, camera):
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(self))
