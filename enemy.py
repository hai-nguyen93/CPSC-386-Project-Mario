import pygame
from pygame.sprite import Sprite
from timer import Timer
from pygame.font import Font

# Add fire stick with boss tag and deleted (re: 'return' only) die function
'''
Fire stick is a list of images
coordinates are based off of sin and cos values for current angle
multiple coefficients by the radius of each fireball
'''


def load(image):
    return pygame.image.load(image)


class Enemy(Sprite):
    def __init__(self, screen, settings, frames, point, left, bot):
        super().__init__()
        self.tag = 'enemy'
        self.screen = screen
        self.settings = settings
        self.anim = Timer(frames)
        self.rect = frames[0].get_rect()
        self.rect.x = left
        self.rect.bottom = bot
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.point = point
        self.dead = False
        self.font = Font(None, 16)
        self.point_text = self.font.render(str(self.point), True, (255, 255, 255), self.settings.bg_color)
        self.point_rect = self.point_text.get_rect()
        self.point_rect.center = self.rect.center
        self.point_time = 1000
        self.point_start_time = 0

    def set_pos(self, left, bot):
        self.rect.x = left
        self.rect.y = bot
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    # General functionality called gethit that updates enemy logic based on state
    def hit(self, player):
        pass

    def die(self):
        self.dead = True
        self.point_start_time = pygame.time.get_ticks()

    def update(self, player, sprites, enemies):
        if self.dead:
            if pygame.time.get_ticks() - self.point_start_time >= self.point_time:
                self.kill()

    def draw(self, camera):
        if self.dead:
            image = self.point_text
        else:
            image = self.anim.imagerect()
        self.screen.blit(image, camera.apply(self))


class Goomba(Enemy):
    def __init__(self, screen, settings, left, bot, altframes=False):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        if not altframes:
            self.frames = [pygame.image.load('images/enemy/goomba1.bmp'),
                           pygame.image.load('images/enemy/goomba2.bmp')]
        else:
            self.frames = [load('images/Enemies/74.png'), load('images/Enemies/75.png')]
        super().__init__(screen=screen, settings=settings, frames=self.frames, point=100, left=left, bot=bot)

        self.is_grounded = False
        self.chasing_player = False
        self.speed = .5
        self.gravity = 0.3
        self.vely = 0
        self.m_dangerous = True
        self.e_dangerous = False

    def update(self, player, sprites, enemies):
        super().update(player, sprites, enemies)

        # check falling off
        if self.rect.y > self.screen_rect.height:
            self.kill()

        # gravity
        if not self.is_grounded:
            self.vely += self.gravity
            if self.vely >= 6:
                self.vely = 6
        else:
            if self.rect.x - player.rect.x < 350:
                self.chasing_player = True
            if self.chasing_player and not self.dead:
                self.x -= self.speed

        self.y += self.vely
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # collision
        self.is_grounded = False
        sprites_hit = pygame.sprite.spritecollide(self, sprites, False)
        if sprites_hit:
            for s in sprites_hit:
                # Enemy, ground can't be broke, brick can, pipe is pipe
                if s.tag in ['brick', 'ground', 'pipe', 'mystery', 'bridge']:
                    c = self.rect.clip(s.rect)  # collision rect
                    if c.width >= c.height:
                        if self.vely >= 0:
                            self.rect.bottom = s.rect.top + 1
                            self.y = float(self.rect.y)
                            self.is_grounded = True
                            self.vely = 0
                    if c.width < c.height:
                        self.speed *= -1
                        self.x -= self.speed
                        self.rect.x = int(self.x)

        collisions = pygame.sprite.spritecollide(self, enemies, False)
        if collisions:
            for enemy in collisions:
                if enemy != self:
                    if enemy.e_dangerous:
                        self.die()
                    else:
                        self.speed *= -1
                        self.x -= self.speed
                        self.rect.x = int(self.x)

    def hit(self, player):
        self.die()
