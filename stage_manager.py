from tile import *
from enemy import *
from enemy2 import *
from pygame.sprite import Group
from warp_zone import WarpZone
from mystery_box import MysteryBox


class StageManager:
    def __init__(self, screen, settings, stats):
        self.stats = stats
        self.settings = settings
        self.screen = screen
        self.enemies = Group()
        self.platforms = Group()
        self.warp_zones = Group()
        self.boxes = Group()
        self.time_limit = 401000  # 401s
        self.time_start = 0
        self.time_elapsed = 0
        self.bgm = pygame.mixer.Sound('audio/overworld.ogg')

    def update(self, player):
        # time over
        if self.stats.current_stage != self.stats.credits_stage:
            self.time_elapsed = pygame.time.get_ticks() - self.time_start
            if self.time_elapsed >= self.time_limit:
                if not player.dead and not player.stage_clear:
                    player.die()

        for e in self.enemies:
            e.update(player, self.platforms, self.enemies)
        for p in self.platforms:
            p.update(self.platforms)

    def draw(self, camera):
        for p in self.platforms:
            p.draw(camera)
        for e in self.enemies:
            e.draw(camera)
        for b in self.boxes:
            b.draw(camera)
        # for w in self.warp_zones:
        #    w.draw(self.screen, camera)

    def load_stage(self, stage, hud):  # character's position in txt file is left bot coordinate
        self.enemies.empty()
        self.platforms.empty()
        self.warp_zones.empty()
        self.time_start = pygame.time.get_ticks()
        self.time_elapsed = 0
        # set up bg_color
        if stage in [1, 3, 5, 7]:
            self.settings.bg_color = (90, 148, 252)
        if stage in [2, 4, 8]:
            self.settings.bg_color = (0, 0, 0)
        if stage in [6]:
            self.settings.bg_color = (90, 90, 255)
        if stage in [-1, self.stats.credits_stage]:
            self.settings.bg_color = (0, 0, 0)

        # set up tile set
        tile_dict = {
            '-': ['bridge', pygame.image.load('images/Tile/castle_bridge.png')],
            '1': ['cloud_start', pygame.image.load('images/Tile/cloud_start.png')],
            '2': ['cloud', pygame.image.load('images/Tile/cloud.png')],
            '3': ['cloud_end', pygame.image.load('images/Tile/cloud_end.png')],
            '4': ['ground', pygame.image.load('images/Tile/box_hit.png')],
            '5': ['bridge', pygame.image.load('images/Tile/chain.png')],
            '6': ['bush_start', pygame.image.load('images/Tile/bush_start.png')],
            '7': ['bush', pygame.image.load('images/Tile/bush.png')],
            '8': ['bush_end', pygame.image.load('images/Tile/bush_end.png')],
            'b': ['brick', pygame.image.load('images/Tile/brick.png')],
            'r': ['brick', pygame.image.load('images/Tile/brick3.png')],
            'c': ['castle', pygame.image.load('images/Tile/castle.png')],
            'd': ['ground', pygame.image.load('images/Tile/ground2.png')],
            'e': ['ground', pygame.image.load('images/Tile/ground3.png')],
            '|': ['ground', pygame.image.load('images/Tile/coral.png')],
            'i': ['coin', pygame.image.load('images/Tile/coin1.png')],
            'o': ['ground', pygame.image.load('images/Tile/barrier.png')],
            'x': ['ground', pygame.image.load('images/Tile/barrier2.png')],
            'S': ['ground', pygame.image.load('images/Tile/stone.png')],
            'X': ['axe', pygame.image.load('images/Tile/axe.png')],
            't': ['lava', pygame.image.load('images/Tile/lava.png')],
            'T': ['lava', pygame.image.load('images/Tile/lava_top.png')],
            'h': ['brick', pygame.image.load('images/Tile/brick2.png')],
            'g': ['ground', pygame.image.load('images/Tile/ground.png')],
            'p': ['pipe', pygame.image.load('images/Tile/pipe.png')],
            'P': ['pipe', pygame.image.load('images/Tile/pipe_end.png')],
            '[': ['pipe', pygame.image.load('images/Tile/pipe_left.png')],
            '{': ['pipe', pygame.image.load('images/Tile/pipe_end_left.png')],
            'M': ['mountain', pygame.image.load('images/Tile/mountain.png')],
            'm': ['mountain', pygame.image.load('images/Tile/mountain.png')],
            'C': ['mystery', 'coin', pygame.image.load('images/Tile/box.png')],
            'L': ['mystery', 'level_up', pygame.image.load('images/Tile/box.png')],
            'l': ['mystery', '1up_mushroom', pygame.image.load('images/Tile/box.png')],
            's': ['mystery', 'star', pygame.image.load('images/Tile/box.png')],
            'q': ['castle', pygame.image.load('images/Tile/castle2.png')],
            'W': ['tree', pygame.image.load('images/Tile/wood.png')],
            'N': ['ground', pygame.image.load('images/Tile/tree1.png')],
            'J': ['ground', pygame.image.load('images/Tile/tree2.png')],
            'Y': ['ground', pygame.image.load('images/Tile/tree3.png')],
            ';': ['bush', pygame.image.load('images/Tile/small_tree.png')],
            ':': ['bush', pygame.image.load('images/Tile/big_tree.png')],
            '^': ['ground', pygame.image.load('images/Tile/bridge.png')],
            '&': ['fence', pygame.image.load('images/Tile/fence2.png')],
            'F': ['bush', pygame.image.load('images/Tile/fence.png')],
            'w': ['win', pygame.image.load('images/Tile/flag.png')]}

        if stage == 1:
            self.load('stage/stage1.txt', tile_dict)  # build map form txt file
            self.warp_zones.add(WarpZone('start', id_num=1, left=46*16, bot=8*16))
            self.warp_zones.add(WarpZone('end', id_num=1, left=254*16, bot=3*16))
            self.warp_zones.add(WarpZone('start', id_num=2, left=287*16, bot=9*16))
            self.warp_zones.add(WarpZone('end', id_num=2, left=179*16, bot=10*16))
        if stage == 2:
            self.load('stage/stage2.txt', tile_dict)
            self.warp_zones.add(WarpZone('start', id_num=1, left=171 * 16, bot=7 * 16))
            self.warp_zones.add(WarpZone('end', id_num=1, left=215 * 16, bot=10 * 16))
        if stage == 3:
            self.load('stage/stage3.txt', tile_dict)
        if stage == 4:
            self.load('stage/stage4.txt', tile_dict)
        if stage == 5:
            self.load('stage/stage5.txt', tile_dict)
            self.warp_zones.add(WarpZone('start', id_num=1, left=103 * 16, bot=8 * 16))
            self.warp_zones.add(WarpZone('end', id_num=1, left=236 * 16, bot=4 * 16))
            self.warp_zones.add(WarpZone('start', id_num=2, left=253 * 16, bot=10 * 16))
            self.warp_zones.add(WarpZone('end', id_num=2, left=115 * 16, bot=10 * 16))
        if stage == 6:
            self.load('stage/stage6.txt', tile_dict)
        if stage == 7:
            self.load('stage/stage7.txt', tile_dict)
        if stage == 8:
            self.load('stage/stage8.txt', tile_dict)
        if stage == self.stats.credits_stage:  # credits screen
            self.load('stage/credits.txt', tile_dict)
            for i in range(0, 18):
                self.platforms.add(Tile(self.screen, tile_dict['o'][0], tile_dict['o'][1], i * 16, 0))

        # load music
        pygame.mixer.stop()
        if stage in [1, 3, 5, 7]:  # overworld stages
            self.bgm = pygame.mixer.Sound('audio/overworld.ogg')
        elif stage in [2]:  # underground stages
            self.bgm = pygame.mixer.Sound('audio/underground.ogg')
        elif stage in [6]:  # underwater stages
            self.bgm = pygame.mixer.Sound('audio/underwater.ogg')
        elif stage in [4, 8]:
            self.bgm = pygame.mixer.Sound('audio/castle.ogg')
        elif stage == self.stats.credits_stage:  # credits screen
            self.bgm = pygame.mixer.Sound('audio/ending.ogg')
        self.bgm.play(-1)

        # refresh hud
        hud.refresh()

    def load(self, fname, tile_dict):
        with open(fname, 'r') as f:
            row = 1
            for l in f:
                col = 0
                for c in l:
                    # create tiles
                    if c in tile_dict:
                        # small mountain needs offset
                        if c == 'm':
                            self.platforms.add(Tile(
                                self.screen, tile_dict[c][0], tile_dict[c][1], col * 16 - 16, row * 16 + 16))
                        elif c in ['C', 'L', 'l', 's']:
                            box = MysteryBox(self.screen, tile_dict[c][0], tile_dict[c][2], col * 16, row * 16)
                            box.set_item(tile_dict[c][1])
                            self.platforms.add(box)
                        else:
                            self.platforms.add(Tile(self.screen, tile_dict[c][0], tile_dict[c][1], col * 16, row * 16))
                    # create enemy
                    if c == 'G':  # goomba
                        self.enemies.add(Goomba(self.screen, self.settings, col * 16, row * 16))
                    elif c == 'K':
                        self.enemies.add(KoopaTroopaGreen(self.screen, self.settings, col * 16, row * 16))
                    elif c == 'R':
                        self.enemies.add(KoopaTroopaRed(self.screen, self.settings, col * 16, row * 16))
                    elif c == 'A':
                        self.enemies.add(KoopaParatroopaRed(self.screen, self.settings, col * 16, row * 16))
                    elif c == 'I':
                        self.enemies.add(FireBar(self.screen, self.settings, (col-1) * 16, (row-1) * 16))
                    elif c == '!':
                        self.enemies.add(Blooper(self.screen, self.settings, col * 16, row * 16))
                    elif c == 'a':
                        self.enemies.add(PiranhaPlant(self.screen, self.settings, col * 16, row * 16))
                    elif c == 'f':
                        self.enemies.add(Podoboo(self.screen, self.settings, col * 16, row * 16))
                    col += 1
                row += 1
        f.close()

    def spawn_sprite(self, tag, img, x, y):
        if tag == 'coin':
            self.platforms.add(PopupCoin(self.screen, tag, img, x, y))
        elif tag in ['mushroom', '1up_mushroom', 'star']:
            self.platforms.add(Mushroom(self.screen, tag, img, x, y))
        else:
            self.platforms.add(Tile(self.screen, tag, img, x, y))

    def reset(self, hud):
        self.load_stage(self.stats.current_stage, hud)
