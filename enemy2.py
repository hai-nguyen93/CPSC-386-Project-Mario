import pygame
from pygame.sprite import Sprite
from timer import Timer
from pygame.font import Font
import math

# Add fire stick with boss tag and deleted (re: 'return' only) die function
'''
Fire stick is a list of images
coordinates are based off of sin and cos values for current angle
multiple coefficients by the radius of each fireball
'''

'''
add m_dangerous, e_dangerous to denote whether a collision will hit mario, friendly enemy
'''


def load(image):
    return pygame.image.load(image)


def min_num(a, b):
    return a if a < b else b


def max_num(a, b):
    return a if a > b else b


class Enemy2(Sprite):
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
        # self.rect = self.anim.frames[self.anim.frameindex].get_rect()
        _ = player
        _ = sprites
        _ = enemies
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
        self.rect = frames[0].get_rect()

    def changetag(self, tag):
        self.tag = tag

    def changewait(self, wait):
        self.anim.wait = wait


'''
Enemy: Koopa Troopa (Green)
-
Functions: Walk (Left/Right), Shell (Stationary, Moving), 'Wake Up' (Unshell)
`
Special Abilities: None
'''


class KoopaTroopaGreen(Enemy2):
    def __init__(self, screen, settings, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.status = 'walkleft'
        self.m_dangerous = True
        self.e_dangerous = False
        self.shell_time = 0
        self.unshell_time = 0
        self.frames = {
            'walkleft': [load('images/Enemies/87.png'), load('images/Enemies/96.png')],
            'walkright': [load('images/Enemies/106.png'), load('images/Enemies/97.png')],
            'shell': [load('images/Enemies/118.png')],
            'mshell': [load('images/Enemies/118.png')],
            'unshell': [load('images/Enemies/113.png')]
        }
        super().__init__(screen=screen, settings=settings, frames=self.frames[self.status],
                         point=200, left=left, bot=bot)

        self.is_grounded = False
        self.chasing_player = False
        self.speed = 1
        self.gravity = 0.3
        self.vely = 0

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
                if self.status != 'unshell' and self.status != 'shell':
                    self.x -= self.speed
                elif self.status == 'shell':
                    if self.shell_time == 0:
                        self.shell_time = pygame.time.get_ticks()
                    else:
                        if pygame.time.get_ticks() - self.shell_time > 7000:
                            self.status = 'unshell'
                            super().changeframes(self.frames[self.status])
                            self.shell_time = 0
                elif self.status == 'unshell':
                    if self.unshell_time == 0:
                        self.unshell_time = pygame.time.get_ticks()
                    else:
                        if pygame.time.get_ticks() - self.unshell_time > 500:
                            self.speed = 1
                            self.status = 'walkleft'
                            self.m_dangerous = True
                            super().changeframes(self.frames[self.status])
                            self.unshell_time = 0

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
                    original_rect = self.rect
                    c = self.rect.clip(s.rect)  # collision rect
                    if c.width >= c.height:
                        if self.vely >= 0:
                            self.rect.bottom = s.rect.top + 1
                            self.y = float(self.rect.y)
                            self.is_grounded = True
                            self.vely = 0
                    if c.width < c.height:
                        self.rect = original_rect
                        if self.status == 'mshell':
                            self.speed *= -1
                        elif self.x < s.rect.x:
                            if self.status == 'walkright':
                                self.x -= self.speed
                                self.speed *= -1
                                self.status = 'walkleft'
                        else:
                            if self.status == 'walkleft':
                                self.x += self.speed
                                self.speed *= -1
                                self.status = 'walkright'
                        super().changeframes(self.frames[self.status])

        if self.status == 'mshell':
            return

        collisions = pygame.sprite.spritecollide(self, enemies, False)
        if collisions:
            for enemy in collisions:
                if enemy != self:
                    if enemy.e_dangerous and not self.e_dangerous:
                        self.die()
                    else:
                        self.x += self.speed
                        if self.rect.x < enemy.rect.x:
                            if self.status != 'walkleft':
                                self.speed *= -1
                                self.status = 'walkleft'
                        else:
                            if self.status != 'walkright':
                                self.speed *= -1
                                self.status = 'walkright'
                        super().changeframes(self.frames[self.status])

    def hit(self, player):
        _ = player
        if self.status == 'walkright' or self.status == 'walkleft':
            self.status = 'shell'
            self.speed = 0
            self.m_dangerous = False
            super().changeframes(self.frames[self.status])
        elif self.status == 'shell':
            self.status = 'mshell'
            self.speed = 3
            self.m_dangerous = True
            self.e_dangerous = True
            super().changeframes(self.frames[self.status])
        elif self.status == 'mshell' or self.status == 'unshell':
            self.m_dangerous = False
            self.e_dangerous = False
            self.die()


'''
Enemy: Koopa Troopa (Red)
-
Functions: Walk (Left/Right), Shell (Stationary, Moving), 'Wake Up' (Unshell)
`
Special Abilities: Afraid of cliffs
'''


class KoopaTroopaRed(Enemy2):
    def __init__(self, screen, settings, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.status = 'walkleft'
        self.m_dangerous = True
        self.e_dangerous = False
        self.shell_time = 0
        self.unshell_time = 0
        self.frames = {
            'walkleft': [load('images/Enemies/88.png'), load('images/Enemies/95.png')],
            'walkright': [load('images/Enemies/105.png'), load('images/Enemies/98.png')],
            'shell': [load('images/Enemies/117.png')],
            'mshell': [load('images/Enemies/117.png')],
            'unshell': [load('images/Enemies/114.png')]
        }
        super().__init__(screen=screen, settings=settings, frames=self.frames[self.status],
                         point=300, left=left, bot=bot)

        self.is_grounded = False
        self.chasing_player = False
        self.speed = 1
        self.gravity = 0.3
        self.vely = 0

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
            self.y += self.vely
            # Potentially add x distance here
        else:
            if self.rect.x - player.rect.x < 350:
                self.chasing_player = True
            if self.chasing_player and not self.dead:
                if self.status != 'unshell' and self.status != 'shell':
                    self.x -= self.speed
                elif self.status == 'shell':
                    if self.shell_time == 0:
                        self.shell_time = pygame.time.get_ticks()
                    else:
                        if pygame.time.get_ticks() - self.shell_time > 7000:
                            self.status = 'unshell'
                            super().changeframes(self.frames[self.status])
                            self.shell_time = 0
                elif self.status == 'unshell':
                    if self.unshell_time == 0:
                        self.unshell_time = pygame.time.get_ticks()
                    else:
                        if pygame.time.get_ticks() - self.unshell_time > 500:
                            self.speed = 1
                            self.status = 'walkleft'
                            self.m_dangerous = True
                            super().changeframes(self.frames[self.status])
                            self.unshell_time = 0

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # collision
        self.is_grounded = False
        sprites_hit = pygame.sprite.spritecollide(self, sprites, False)
        if sprites_hit:
            for s in sprites_hit:
                # Enemy, ground can't be broke, brick can, pipe is pipe
                if s.tag in ['brick', 'ground', 'pipe', 'mystery']:
                    original_rect = self.rect
                    c = self.rect.clip(s.rect)  # collision rect
                    if c.width >= c.height:
                        if self.vely >= 0:
                            self.rect.bottom = s.rect.top + 1
                            self.y = float(self.rect.y)
                            self.is_grounded = True
                            self.vely = 0
                    if c.width < c.height:
                        self.rect = original_rect
                        if self.status == 'mshell':
                            self.speed *= -1
                        elif self.x < s.rect.x:
                            if self.status == 'walkright':
                                self.x -= self.speed
                                self.speed *= -1
                                self.status = 'walkleft'
                        else:
                            if self.status == 'walkleft':
                                self.x += self.speed
                                self.speed *= -1
                                self.status = 'walkright'
                        super().changeframes(self.frames[self.status])

            if len(sprites_hit) == 1:
                if (self.rect.left <= sprites_hit[0].rect.left - sprites_hit[0].rect.width + 2
                        and self.status == 'walkleft'):
                    self.speed *= -1
                    self.x -= self.speed
                    self.rect.x = int(self.x)
                    self.status = 'walkright'
                    super().changeframes(self.frames[self.status])
                if (self.rect.right >= sprites_hit[0].rect.right + sprites_hit[0].rect.width - 2
                        and self.status == 'walkright'):
                    self.speed *= -1
                    self.x -= self.speed
                    self.rect.x = int(self.x)
                    self.status = 'walkleft'
                    super().changeframes(self.frames[self.status])

        if self.status == 'mshell':
            return

        collisions = pygame.sprite.spritecollide(self, enemies, False)
        if collisions:
            for enemy in collisions:
                if enemy != self:
                    if enemy.e_dangerous and not self.e_dangerous:
                        self.die()
                    else:
                        self.x += self.speed
                        if self.rect.x < enemy.rect.x:
                            if self.status != 'walkleft':
                                self.speed *= -1
                                self.status = 'walkleft'
                        else:
                            if self.status != 'walkright':
                                self.speed *= -1
                                self.status = 'walkright'
                        super().changeframes(self.frames[self.status])

    def hit(self, player):
        if self.status == 'walkright' or self.status == 'walkleft':
            self.status = 'shell'
            self.speed = 0
            self.m_dangerous = False
            super().changeframes(self.frames[self.status])
        elif self.status == 'shell':
            self.status = 'mshell'
            self.speed = 3
            if player.rect.x + player.rect.width // 2 < self.x + self.rect.x // 2:
                self.speed *= -1
            self.m_dangerous = True
            self.e_dangerous = True
            super().changeframes(self.frames[self.status])
        elif self.status == 'mshell' or self.status == 'unshell':
            self.m_dangerous = False
            self.e_dangerous = False
            self.die()


'''
Enemy: Koopa Paratroopa (Red)
-
Functions: Fly, Walk (Left/Right), Shell (Stationary, Moving), 'Wake Up' (Unshell)
`
Special Abilities: Afraid of cliffs, Flying
'''


class KoopaParatroopaRed(Enemy2):
    def __init__(self, screen, settings, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.status = 'fly'
        self.m_dangerous = True
        self.e_dangerous = False
        self.shell_time = 0
        self.unshell_time = 0
        self.frames = {
            'fly': [load('images/Enemies/78.png'), load('images/Enemies/85.png')],
            'walkleft': [load('images/Enemies/88.png'), load('images/Enemies/95.png')],
            'walkright': [load('images/Enemies/105.png'), load('images/Enemies/98.png')],
            'shell': [load('images/Enemies/117.png')],
            'mshell': [load('images/Enemies/117.png')],
            'unshell': [load('images/Enemies/114.png')]
        }
        super().__init__(screen=screen, settings=settings, frames=self.frames[self.status],
                         point=500, left=left, bot=bot)

        self.is_grounded = False
        self.chasing_player = False
        self.speed = 0.2
        self.gravity = 0.3
        self.vely = 0
        self.oy = self.y
        self.yrange = 64

    def update(self, player, sprites, enemies):
        super().update(player, sprites, enemies)

        # check falling off
        if self.rect.y > self.screen_rect.height:
            self.kill()

        if self.status == 'fly':
            if self.y < self.oy - self.yrange:
                self.speed *= -1
            elif self.y > self.oy + self.yrange:
                self.speed *= -1
            self.y += self.speed

        else:
            if not self.is_grounded:
                self.vely += self.gravity
                if self.vely >= 6:
                    self.vely = 6
                self.y += self.vely
                # Potentially add x distance here
            else:
                if self.rect.x - player.rect.x < 350:
                    self.chasing_player = True
                if self.chasing_player and not self.dead:
                    if self.status != 'unshell' and self.status != 'shell':
                        self.x -= self.speed
                    elif self.status == 'shell':
                        if self.shell_time == 0:
                            self.shell_time = pygame.time.get_ticks()
                        else:
                            if pygame.time.get_ticks() - self.shell_time > 7000:
                                self.status = 'unshell'
                                super().changeframes(self.frames[self.status])
                                self.shell_time = 0
                    elif self.status == 'unshell':
                        if self.unshell_time == 0:
                            self.unshell_time = pygame.time.get_ticks()
                        else:
                            if pygame.time.get_ticks() - self.unshell_time > 500:
                                self.speed = 1
                                self.status = 'walkleft'
                                self.m_dangerous = True
                                super().changeframes(self.frames[self.status])
                                self.unshell_time = 0

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if self.status == 'fly':
            return

        # collision
        self.is_grounded = False
        sprites_hit = pygame.sprite.spritecollide(self, sprites, False)
        if sprites_hit:
            for s in sprites_hit:
                # Enemy, ground can't be broke, brick can, pipe is pipe
                if s.tag in ['brick', 'ground', 'pipe', 'mystery']:
                    original_rect = self.rect
                    c = self.rect.clip(s.rect)  # collision rect
                    if c.width >= c.height:
                        if self.vely >= 0:
                            self.rect.bottom = s.rect.top + 1
                            self.y = float(self.rect.y)
                            self.is_grounded = True
                            self.vely = 0
                    if c.width < c.height:
                        self.rect = original_rect
                        if self.status == 'mshell':
                            self.speed *= -1
                        elif self.x < s.rect.x:
                            if self.status == 'walkright':
                                self.x -= self.speed
                                self.speed *= -1
                                self.status = 'walkleft'
                        else:
                            if self.status == 'walkleft':
                                self.x += self.speed
                                self.speed *= -1
                                self.status = 'walkright'
                        super().changeframes(self.frames[self.status])

            if len(sprites_hit) == 1:
                if (self.rect.left <= sprites_hit[0].rect.left - sprites_hit[0].rect.width + 2
                        and self.status == 'walkleft'):
                    self.speed *= -1
                    self.x -= self.speed
                    self.rect.x = int(self.x)
                    self.status = 'walkright'
                    super().changeframes(self.frames[self.status])
                if (self.rect.right >= sprites_hit[0].rect.right + sprites_hit[0].rect.width - 2
                        and self.status == 'walkright'):
                    self.speed *= -1
                    self.x -= self.speed
                    self.rect.x = int(self.x)
                    self.status = 'walkleft'
                    super().changeframes(self.frames[self.status])

        if self.status == 'mshell':
            return

        collisions = pygame.sprite.spritecollide(self, enemies, False)
        if collisions:
            for enemy in collisions:
                if enemy != self:
                    if enemy.e_dangerous and not self.e_dangerous:
                        self.die()
                    else:
                        self.x += self.speed
                        if self.rect.x < enemy.rect.x:
                            if self.status != 'walkleft':
                                self.speed *= -1
                                self.status = 'walkleft'
                        else:
                            if self.status != 'walkright':
                                self.speed *= -1
                                self.status = 'walkright'
                        super().changeframes(self.frames[self.status])

    def hit(self, player):
        if self.status == 'fly':
            self.status = 'walkleft'
            self.speed = 1
            super().changeframes(self.frames[self.status])
        elif self.status == 'walkright' or self.status == 'walkleft':
            self.status = 'shell'
            self.speed = 0
            self.m_dangerous = False
            super().changeframes(self.frames[self.status])
        elif self.status == 'shell':
            self.status = 'mshell'
            self.speed = 3
            if player.rect.x + player.rect.width // 2 < self.x + self.rect.x // 2:
                self.speed *= -1
            self.m_dangerous = True
            self.e_dangerous = True
            super().changeframes(self.frames[self.status])
        elif self.status == 'mshell' or self.status == 'unshell':
            self.m_dangerous = False
            self.e_dangerous = False
            self.die()


'''
Enemy: Piranha Plant
-
Functions: Rise/Fall
`
Special Abilities: None
'''


class PiranhaPlant(Enemy2):
    def __init__(self, screen, settings, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.m_dangerous = True
        self.e_dangerous = False
        self.frames = [load('images/Enemies/121.png'), load('images/Enemies/122.png')]
        super().__init__(screen=screen, settings=settings, frames=self.frames,
                         point=200, left=left, bot=bot)

        self.is_grounded = False
        self.chasing_player = False
        self.speed = -0.1
        self.max_y = self.y + 28
        self.min_y = self.y
        self.original_y = int(self.y) + 1
        self.x += 8
        self.y += 1

    def update(self, player, sprites, enemies):
        super().update(player, sprites, enemies)

        if self.rect.x - player.rect.x < 350:
            self.chasing_player = True
        if self.chasing_player and not self.dead:
            if self.y <= self.min_y:
                self.speed *= -1
            elif self.y >= self.max_y:
                self.speed *= -1
            self.y += self.speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def hit(self, player):
        _ = player
        self.die()

    def draw(self, camera):
        if self.dead:
            image = self.point_text
            self.screen.blit(image, camera.apply(self))
        else:
            image = self.anim.imagerect()
            height = 24 - (self.rect.y - self.original_y)
            # Clip part of the image based on how far above ground it should be
            if height > 0:
                self.screen.blit(image, camera.apply(self), (0, 0, self.rect.width, height))


'''
Enemy: Podoboo
-
Functions: Rise/Fall
`
Special Abilities: None
'''


class Podoboo(Enemy2):
    def __init__(self, screen, settings, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.m_dangerous = True
        self.e_dangerous = False
        self.status = 'up'
        self.waittime = pygame.time.get_ticks()
        self.waiting = True
        self.frames = {
            'up': [load('images/Enemies/56.png')],
            'down': [load('images/Enemies/61.png')]
        }
        super().__init__(screen=screen, settings=settings, frames=self.frames[self.status],
                         point=0, left=left, bot=bot)

        self.chasing_player = False
        self.speed = -2
        self.miny = 100
        self.y = self.settings.scr_height

    def update(self, player, sprites, enemies):
        super().update(player, sprites, enemies)

        if self.rect.x - player.rect.x < 350:
            self.chasing_player = True
        if self.chasing_player and not self.dead:
            if self.waiting:
                if pygame.time.get_ticks() - self.waittime >= 4000:
                    self.waiting = False
            else:
                if self.y < self.miny + 10:
                    if self.speed >= 0:
                        self.speed = 1
                    else:
                        self.speed = -1
                else:
                    if self.speed >= 0:
                        self.speed = 2
                    else:
                        self.speed = -2
                if self.y < self.miny:
                    self.status = 'down'
                    super().changeframes(self.frames[self.status])
                    self.speed *= -1
                elif self.y > self.settings.scr_height:
                    self.status = 'up'
                    super().changeframes(self.frames[self.status])
                    self.speed *= -1
                    self.waittime = pygame.time.get_ticks()
                    self.waiting = True
                self.y += self.speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def hit(self, player):
        _ = player
        self.die()


'''
Enemy: Blooper
-
Functions: Rise/Fall
`
Special Abilities: Won't directly target Mario

Notes: X movement is 4 blocks at a time
       Y movement is 8 block at a time, 1 block above Mario min
'''


class Blooper(Enemy2):
    def __init__(self, screen, settings, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.status = 'up'
        self.m_dangerous = True
        self.e_dangerous = False
        self.frames = {
            'up': [load('images/Enemies/124.png')],
            'down': [load('images/Enemies/119.png')]
        }
        super().__init__(screen=screen, settings=settings, frames=self.frames[self.status],
                         point=500, left=left, bot=bot)

        self.chasing_player = False
        self.base_loc = self.rect

    def update(self, player, sprites, enemies):
        super().update(player, sprites, enemies)

        if self.rect.x - player.rect.x < 500:
            self.chasing_player = True
        if self.chasing_player and not self.dead:
            # Determine which set of actions to take based on base location and player location
            if self.base_loc.x > player.x:
                if abs(self.x - player.x) < 64 and self.x == self.base_loc.x:
                    if player.y < 64:
                        miny = 0
                        maxy = 64
                    elif 64 < player.y < self.settings.scr_height - 64:
                        miny = max_num(player.y - 80, 0)
                        maxy = min_num(player.y + 16, self.settings.scr_height - 64)
                    else:
                        miny = player.y - player.rect.height - 80
                        maxy = player.y - player.rect.height - 16
                    if self.y < miny:
                        self.y += 1
                        self.status = 'down'
                        super().changeframes(self.frames[self.status])
                    elif self.y > maxy:
                        self.y -= 1
                        self.status = 'up'
                        super().changeframes(self.frames[self.status])
                    else:
                        if self.status == 'up':
                            self.y -= 1
                        else:
                            self.y += 1
                # Check Blooper location relative to base location
                elif abs(self.base_loc.x - self.x) < 64:
                    self.x -= 1
                    self.y -= 1
                    self.status = 'up'
                    super().changeframes(self.frames[self.status])
                else:
                    if self.y > min_num(player.y + player.rect.height, self.base_loc.y):
                        self.base_loc = self.rect
                    else:
                        self.y += 1
                        self.status = 'down'
                        super().changeframes(self.frames[self.status])
            else:
                if abs(self.x - player.x) < 64 and self.x == self.base_loc.x:
                    if player.y < 64:
                        miny = 0
                        maxy = 64
                    elif 64 < player.y < self.settings.scr_height - 64:
                        miny = max_num(player.y - 80, 0)
                        maxy = min_num(player.y + 16, self.settings.scr_height - 64)
                    else:
                        miny = player.y - player.rect.height - 80
                        maxy = player.y - player.rect.height - 16
                    if self.y < miny:
                        self.y += 1
                        self.status = 'down'
                        super().changeframes(self.frames[self.status])
                    elif self.y > maxy:
                        self.y -= 1
                        self.status = 'up'
                        super().changeframes(self.frames[self.status])
                    else:
                        if self.status == 'up':
                            self.y -= 1
                        else:
                            self.y += 1
                # Check Blooper location relative to base location
                elif abs(self.base_loc.x - self.x) < 64:
                    self.x += 1
                    self.y -= 1
                    self.status = 'up'
                    super().changeframes(self.frames[self.status])
                else:
                    if self.y > min_num(player.y + player.rect.height, self.base_loc.y):
                        self.base_loc = self.rect
                    else:
                        self.y += 1
                        self.status = 'down'
                        super().changeframes(self.frames[self.status])

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def hit(self, player):
        _ = player
        self.die()


'''
Enemy: Fire-Bar
-
Functions: Rotate
`
Special Abilities: None
'''


class FireBar(Enemy2):
    def __init__(self, screen, settings, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.m_dangerous = True
        self.e_dangerous = False
        self.player = None
        self.frames = [
            load('images/Enemies/147.png'),
            pygame.transform.rotate(load('images/Enemies/147.png'), 90),
            pygame.transform.rotate(load('images/Enemies/147.png'), 180),
            pygame.transform.rotate(load('images/Enemies/147.png'), 270),
        ] * 12

        super().__init__(screen=screen, settings=settings, frames=self.frames,
                         point=0, left=left, bot=bot)

        self.basex = self.rect.x + 4
        self.basey = self.rect.y + 12

        # center on below = +4, +12

        super().changetag('boss')
        # super().changewait(200)

    def update(self, player, sprites, enemies):
        super().update(player, sprites, enemies)
        self.player = player

    def hit(self, player):
        _ = player
        self.kill()

    def draw(self, camera):
        image = self.anim.imagerect()
        index = self.anim.frameindex // 2
        for radius in range(0, 40, 8):
            self.rect.x = self.basex + math.cos(math.radians(index * -15)) * radius
            self.rect.y = self.basey + math.sin(math.radians(index * -15)) * radius
            self.screen.blit(image, camera.apply(self))

        base_rect = pygame.Rect(self.basex - 4, self.basey + 4, 8, 8)
        self.rect = base_rect.union(pygame.Rect(self.rect.x, self.rect.y, 8, 8))
        # pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
