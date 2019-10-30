from pygame.font import Font


class HelpText:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.font = Font(None, 30)
        self.msg = 'A/D: move left/right    Left-Shift: run'
        self.msg2 = 'W: jump    S: crouch    Space: fire'
        self.text = self.font.render(self.msg, True, (255, 255, 255), self.settings.bg_color)
        self.rect = self.text.get_rect()
        self.text2 = self.font.render(self.msg2, True, (255, 255, 255), self.settings.bg_color)
        self.rect2 = self.text2.get_rect()
        self.rect.x = self.rect2.x = 17
        self.rect.top = 100
        self.rect2.top = self.rect.bottom + 2

    def draw(self, camera):
        self.screen.blit(self.text, camera.apply(self))
        self.screen.blit(self.text2, self.rect2.move(camera.rect.topleft))
