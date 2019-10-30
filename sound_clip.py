import pygame


class SoundClip:
    def __init__(self, sound_file_name):
        self.clip = pygame.mixer.Sound(sound_file_name)
        self.finished = False
        self.length = self.clip.get_length() * 1000
        self.start_time = 0

    def play(self):
        self.clip.play()
        self.finished = False
        self.start_time = pygame.time.get_ticks()

    def is_finished(self):
        self.finished = ((pygame.time.get_ticks() - self.start_time) >= self.length)
        return self.finished
