from pygame.font import Font


class GameoverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font = Font(None, 40)
        self.text_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.text = self.font.render('Game Over', True, self.text_color, self.bg_color)
        self.text1 = self.font.render('Press ESC to quit.', True, self.text_color, self.bg_color)
        self.text_rect = self.text.get_rect()
        self.text1_rect = self.text1.get_rect()
        self.text_rect.center = self.screen_rect.center
        self.text1_rect.centerx = self.screen_rect.centerx
        self.text1_rect.top = self.text_rect.bottom + 5

    def draw(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.text, self.text_rect)
        self.screen.blit(self.text1, self.text1_rect)
