import pygame


class Camera:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(0, 0, self.screen_rect.width, self.screen_rect.height)
        self.x = float(self.rect.x)

    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, target):
        if target.rect.x + self.rect.x >= int(self.screen_rect.width/2.5):
            if target.vel.x >= 0:
                self.x += -target.vel.x
        # elif self.rect.x + target.rect.x < 100:
        #    self.x += 4

        # self.x += self.vel_x
        self.rect.x = int(self.x)

        # self.rect.x = -target.rect.x + (self.settings.scr_width/2)
        # print('{}_____{}'.format(str(self.rect.x), str(target.rect.x)))
        # self.rect.y = -target.rect.y + 300

    def out_of_camera(self, target):
        return self.rect.x + target.rect.x < 0

    def set_pos(self, dest_x):
        self.rect.x = -(dest_x - 17)
        self.x = float(self.rect.x)

    def reset(self):
        self.rect.x = self.rect.y = 0
        self.x = float(self.rect.x)
