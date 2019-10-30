import pygame
from timer import Timer
from pygame.font import Font


class CreditsScreen:
    def __init__(self, screen):
        self.bg_color = (0, 0, 0)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bowsette = Timer([pygame.image.load('images/player/bowsette1.png'),
                               pygame.image.load('images/player/bowsette2.png'),
                               pygame.image.load('images/player/bowsette3.png'),
                               pygame.image.load('images/player/bowsette4.png')], wait=200)
        self.bowsette_rect = self.bowsette.frames[0].get_rect()
        self.font = Font(None, 32)
        self.text_color = (255, 255, 255)
        self.text = self.font.render('Thank you for playing.', True, self.text_color, self.bg_color)
        self.text_rect = self.text.get_rect()
        self.text_box_color = (255, 255, 255)
        self.text_box = pygame.Rect(0, 0, self.text_rect.width + 5, self.text_rect.height + 5)
        self.text_box.centerx = 510
        self.text_box.centery = 550
        self.text_rect.center = self.text_box.center
        self.bowsette_rect.bottom = 625
        self.bowsette_rect.centerx = self.text_rect.centerx
        self.bg_image = pygame.image.load('images/credits_screen.png')
        # self.bg_image = pygame.transform.scale(self.bg_image, self.screen_rect.size)

    def draw(self):
        self.screen.fill(self.text_box_color, self.text_box)
        self.screen.blit(self.bg_image, self.screen_rect)
        self.screen.blit(self.text, self.text_rect)
        self.screen.blit(self.bowsette.imagerect(), self.bowsette_rect)
