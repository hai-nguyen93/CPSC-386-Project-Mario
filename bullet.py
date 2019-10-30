import pygame
from pygame.sprite import Sprite
from timer import Timer


class Bullet(Sprite):
    def __init__(self, screen, direction, x, y):
        super().__init__()
        self.screen = screen
        self.speed = 6
        self.max_distace = 600
        self.traveled_distance = 0
        self.direction = direction
        self.anim = Timer([pygame.image.load('images/player/fire1.bmp'),
                           pygame.image.load('images/player/fire2.bmp'),
                           pygame.image.load('images/player/fire3.bmp'),
                           pygame.image.load('images/player/fire4.bmp')])
        self.rect = self.anim.frames[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)

    def update(self, player, platforms, enemies):
        if self.traveled_distance >= self.max_distace:
            self.kill()
        else:
            self.x += (self.direction * self.speed)
            self.traveled_distance += self.speed
            self.rect.x = int(self.x)

            # check collision with enemies
            hit = pygame.sprite.spritecollideany(self, enemies)
            if hit:
                if not hit.dead:
                    player.stats.score += hit.point
                    player.hud.prep_score()
                    self.kill()
                    hit.get_hit()

            # check collision with platforms
            hit = pygame.sprite.spritecollideany(self, platforms)
            if hit:
                if hit.tag in ['ground', 'pipe', 'brick']:
                    self.kill()

    def draw(self, camera):
        self.screen.blit(self.anim.imagerect(), camera.apply(self))
