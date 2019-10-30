from pygame.font import Font


class HUD:
    def __init__(self, screen, settings, stats, stage_manager):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.sm = stage_manager
        self.font = Font(None, 26)
        self.text_color = (255, 255, 255)

        # score
        self.score_text = self.font.render('Score: ' + str(int(self.stats.score)), True, self.text_color,
                                           self.settings.bg_color)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.left = 10
        self.score_rect.bottom = int(self.screen_rect.height / 20)

        # stage
        self.stage_text = self.font.render('Stage: ' + str(self.stats.current_stage), True, self.text_color,
                                           self.settings.bg_color)
        self.stage_rect = self.stage_text.get_rect()
        self.stage_rect.left = int(self.screen_rect.width * 0.84)
        self.stage_rect.bottom = self.score_rect.bottom

        # coins
        self.coins_text = self.font.render('Coin: ' + str(self.stats.coins), True, self.text_color,
                                           self.settings.bg_color)
        self.coins_rect = self.coins_text.get_rect()
        self.coins_rect.left = int(self.screen_rect.width * 0.3)
        self.coins_rect.bottom = self.score_rect.bottom

        # Time
        self.time_text = self.font.render('Time: ' + str((self.sm.time_limit - self.sm.time_elapsed)//1000),
                                          True, self.text_color, self.settings.bg_color)
        self.time_rect = self.time_text.get_rect()
        self.time_rect.bottom = self.score_rect.bottom
        self.time_rect.left = int(self.screen_rect.width * 0.55)

        # lives
        self.lives_text = self.font.render('Lives: ' + str(self.stats.lives_left), True, self.text_color,
                                           self.settings.bg_color)
        self.lives_rect = self.lives_text.get_rect()
        self.lives_rect.left = self.score_rect.left
        self.lives_rect.top = self.score_rect.bottom + 5

    def prep_coins(self):
        self.coins_text = self.font.render('Coin: ' + str(self.stats.coins), True, self.text_color,
                                           self.settings.bg_color)
        self.coins_rect = self.coins_text.get_rect()
        self.coins_rect.left = int(self.screen_rect.width * 0.3)
        self.coins_rect.bottom = self.score_rect.bottom

    def prep_score(self):
        self.score_text = self.font.render('Score:' + str(int(self.stats.score)), True, self.text_color,
                                           self.settings.bg_color)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.left = 10
        self.score_rect.bottom = int(self.screen_rect.height / 20)

    def prep_stage(self):
        self.stage_text = self.font.render('STAGE: ' + str(self.stats.current_stage), True, self.text_color,
                                           self.settings.bg_color)
        self.stage_rect = self.stage_text.get_rect()
        self.stage_rect.left = int(self.screen_rect.width * 0.84)
        self.stage_rect.bottom = self.score_rect.bottom

    def prep_lives(self):
        self.lives_text = self.font.render('Lives: ' + str(self.stats.lives_left), True, self.text_color,
                                           self.settings.bg_color)
        self.lives_rect = self.lives_text.get_rect()
        self.lives_rect.left = self.score_rect.left
        self.lives_rect.top = self.score_rect.bottom + 5

    def prep_time(self):
        time = self.sm.time_limit - self.sm.time_elapsed
        if time < 0:
            time = 0
        self.time_text = self.font.render('Time: ' + str(time//1000),
                                          True, self.text_color, self.settings.bg_color)
        self.time_rect = self.time_text.get_rect()
        self.time_rect.bottom = self.score_rect.bottom
        self.time_rect.left = int(self.screen_rect.width * 0.55)

    def refresh(self):
        self.prep_lives()
        self.prep_score()
        self.prep_time()
        self.prep_stage()
        self.prep_coins()

    def draw(self):
        self.screen.blit(self.score_text, self.score_rect)
        self.screen.blit(self.stage_text, self.stage_rect)
        self.screen.blit(self.coins_text, self.coins_rect)
        self.screen.blit(self.lives_text, self.lives_rect)
        self.prep_time()
        self.screen.blit(self.time_text, self.time_rect)
