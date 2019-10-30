import pygame
from pygame.sprite import Sprite
from timer import Timer
from pygame.font import Font


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
        self.detect_range = 200

    def set_pos(self, left, bot):
        self.rect.x = left
        self.rect.y = bot
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def get_hit(self):
        self.die()

    def die(self):
        self.dead = True
        self.point_start_time = pygame.time.get_ticks()

    def update(self, player, sprites):
        if self.dead:
            if pygame.time.get_ticks() - self.point_start_time >= self.point_time:
                self.kill()

    def draw(self, camera):
        if self.dead:
            image = self.point_text
        else:
            image = self.anim.imagerect()
        self.screen.blit(image, camera.apply(self))

    def changeframes(self, frames):
        self.anim = Timer(frames)


class Goomba(Enemy):
    def __init__(self, screen, settings, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.frames = [pygame.image.load('images/enemy/goomba1.bmp'),
                       pygame.image.load('images/enemy/goomba2.bmp')]
        super().__init__(screen=screen, settings=settings, frames=self.frames, point=100, left=left, bot=bot)

        self.is_grounded = False
        self.chasing_player = False
        self.speed = 1
        self.gravity = 0.3
        self.vely = 0

    def update(self, player, sprites):
        super().update(player, sprites)

        # check falling off
        if self.rect.y > self.screen_rect.height:
            self.kill()

        # gravity
        if not self.is_grounded:
            self.vely += self.gravity
            if self.vely >= 6:
                self.vely = 6
        else:
            if self.rect.x - player.rect.x < self.detect_range:
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
                        self.x -= self.speed
                        self.rect.x = int(self.x)


class KoopaTroopa(Enemy):
    def __init__(self, screen, settings, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.status = 'walkleft'
        self.animations = {
            'walkleft': [load('images/Enemies/87.png'), load('images/Enemies/96.png')],
            'walkright': [load('images/Enemies/106.png'), load('images/Enemies/97.png')],
            'shell': [load('images/Enemies/118.png')],
            'unshell': [load('images/Enemies/113.png')]
        }
        super().__init__(screen=screen, settings=settings, frames=self.animations[self.status],
                         point=100, left=left, bot=bot)
        self.is_grounded = False
        self.chasing_player = False
        self.speed = 1
        self.gravity = 0.3
        self.vely = 0

    def update(self, player, sprites):
        super().update(player, sprites)

        # check falling off
        if self.rect.y > self.screen_rect.height:
            self.kill()

        # gravity
        if not self.is_grounded:
            self.vely += self.gravity
            if self.vely >= 6:
                self.vely = 6
        else:
            if self.rect.x - player.rect.x < self.detect_range:
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
                        self.x -= self.speed
                        self.rect.x = int(self.x)
                        if self.status == 'walkleft':
                            self.status = 'walkright'
                        elif self.status == 'walkright':
                            self.status = 'walkleft'
                        super().changeframes(self.animations[self.status])
            if len(sprites_hit) == 1:
                if self.rect.left <= sprites_hit[0].rect.left - sprites_hit[0].rect.width + 2:
                    self.speed *= -1
                    self.x -= self.speed
                    self.rect.x = int(self.x)
                if self.rect.right >= sprites_hit[0].rect.right + sprites_hit[0].rect.width - 2:
                    self.speed *= -1
                    self.x -= self.speed
                    self.rect.x = int(self.x)
