import pygame
from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, screen, tag, image, left, bot):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = image
        self.rect = self.image.get_rect()
        self.tag = tag
        self.rect.x = left
        self.rect.bottom = bot

    def update(self, sprites):
        pass

    def draw(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class PopupCoin(Tile):
    def __init__(self, screen, tag, image, left, bot):
        super().__init__(screen, tag, image, left, bot)
        self.max_distance = 16
        self.travel_distance = 0
        self.y = float(self.rect.y)

    def update(self, sprites):
        self.y -= 1
        self.travel_distance += 1
        self.rect.y = int(self.y)
        if self.travel_distance >= self.max_distance:
            self.kill()


class Mushroom(Tile):
    def __init__(self, screen, tag, image, left, bot):
        super().__init__(screen, tag, image, left, bot)
        self.is_grounded = False
        self.speed = 1
        self.gravity = 0.3
        self.vely = 0
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, sprites):
        # check falling off
        if self.rect.y > self.screen_rect.height:
            self.kill()

        # gravity
        if not self.is_grounded:
            self.vely += self.gravity
            if self.vely >= 6:
                self.vely = 6

        self.y += self.vely
        self.x += self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # collision
        self.is_grounded = False
        sprites_hit = pygame.sprite.spritecollide(self, sprites, False)
        if sprites_hit:
            for s in sprites_hit:
                if s.tag in ['brick', 'ground', 'pipe', 'mystery']:
                    c = self.rect.clip(s.rect)  # collision rect
                    if c.width >= c.height:
                        if self.vely >= 0:
                            self.rect.bottom = s.rect.top + 1
                            self.y = float(self.rect.y)
                            self.is_grounded = True
                            self.vely = 0
                    if c.width < c.height:
                        self.speed *= -1
                        self.x += self.speed
                        self.rect.x = int(self.x)
