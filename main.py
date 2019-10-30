from settings import Settings
import game_functions as gf
from player import Player
from camera import Camera
from hud import HUD
from game_stats import GameStats
from enemy import *
from stage_manager import StageManager
from credits import CreditsScreen
from gameover import GameoverScreen
from help import HelpText

FPS = 60


def play():
    pygame.init()
    settings = Settings()
    window = pygame.display.set_mode((768, 672), 0, 32)  # window's resolution
    screen = pygame.Surface((settings.scr_width, settings.scr_height))  # real game's resolution
    pygame.display.set_caption("Mario")
    stats = GameStats()
    main_clock = pygame.time.Clock()
    cs = CreditsScreen(screen=window)
    go = GameoverScreen(screen=window)
    camera = Camera(screen=screen)
    sm = StageManager(screen=screen, settings=settings, stats=stats)
    hud = HUD(screen=window, settings=settings, stats=stats, stage_manager=sm)
    pc = Player(screen=screen, settings=settings, stats=stats, stage_manager=sm, camera=camera, hud=hud)
    sm.load_stage(stage=stats.current_stage, hud=hud)
    help_text = HelpText(screen=window, settings=settings)
    pygame.mouse.set_visible(False)

    # Main loop
    while True:
        # scale the game's resolution to window's resolution
        resized = pygame.transform.scale(screen, (768, 672))
        window.blit(resized, (0, 0))

        gf.check_inputs(player=pc)

        if stats.current_stage < stats.credits_stage and stats.current_stage != -1:
            camera.update(pc)
        if stats.current_stage != -1:
            gf.update_player(player=pc, platforms=sm.platforms, enemies=sm.enemies, warp_zones=sm.warp_zones)
            sm.update(player=pc)

        # draw
        if stats.current_stage != -1:
            screen.fill(settings.bg_color)
            sm.draw(camera)
            pc.draw1()

        if stats.current_stage < stats.credits_stage and stats.current_stage != -1:
            hud.draw()
            if stats.current_stage == 1:
                help_text.draw(camera)
        elif stats.current_stage == stats.credits_stage:
            cs.draw()
        elif stats.current_stage == -1:
            go.draw()
        pygame.display.update()
        main_clock.tick(60)


play()
