class GameStats:
    def __init__(self):
        self.game_status = 0  # 0: menu, 1: game active
        self.current_stage = 1
        self.swim_stage = 6
        self.credits_stage = 9
        self.score = 0
        self.coins = 0
        self.lives_left = 3

    def reset(self):
        self.game_status = 0
        self.current_stage = 1
        self.score = 0
        self.lives_left = 3

    def update_coins(self):
        if self.coins >= 100:
            self.coins -= 100
            self.lives_left += 1
