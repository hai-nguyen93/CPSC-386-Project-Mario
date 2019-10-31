from pygame.sprite import Sprite


class MysteryBox(Sprite):
    def __init__(self, screen, tag, image, left, bottom):
        super().__init__()
        self.screen = screen
        self.image = image
        self.tag = tag
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.bottom = bottom
        self.item = None

    def set_item(self, item):
        self.item = item

    def draw(self, camera):
        self.screen.blit(self.image, camera.apply(self))
