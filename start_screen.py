import pygame
from pygame.font import Font


class StartScreen:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font = Font(None, 56)
        self.text_color = (250, 150, 150)

        # Title
        self.title1_text = self.font.render("FAKE", True, self.text_color, self.settings.bg_color)
        self.title1_rect = self.title1_text.get_rect()
        self.title2_text = self.font.render("MARIO", True, self.text_color, self.settings.bg_color)
        self.title2_rect = self.title2_text.get_rect()
        self.title3_text = self.font.render("CLONE", True, self.text_color, self.settings.bg_color)
        self.title3_rect = self.title3_text.get_rect()
        self.title1_rect.centerx = self.title2_rect.centerx = self.title3_rect.centerx = self.screen_rect.centerx
        self.title1_rect.centery = self.screen_rect.height / 5
        self.title2_rect.y = self.title1_rect.bottom + 20
        self.title3_rect.y = self.title2_rect.bottom + 20

    def draw(self):
        self.screen.blit(self.title1_text, self.title1_rect)
        self.screen.blit(self.title2_text, self.title2_rect)
        self.screen.blit(self.title3_text, self.title3_rect)
