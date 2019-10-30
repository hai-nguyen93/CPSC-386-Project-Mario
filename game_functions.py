import pygame
import sys
from pygame.locals import *


RIGHT_KEYS = [K_d, K_RIGHT]
LEFT_KEYS = [K_a, K_LEFT]


def terminate():
    pygame.quit()
    sys.exit()


def check_inputs(player):
    for e in pygame.event.get():
        if e.type == QUIT:
            terminate()
        elif e.type == KEYDOWN:
            check_keydown(e, player)
        elif e.type == KEYUP:
            check_keyup(e, player)


def check_keydown(event, player):
    if event.key in [K_UP, K_w]:
        player.jump()
    if event.key == K_SPACE:
        player.fire()


def check_keyup(event, player):
    if event.key == K_ESCAPE:
        terminate()


def update_player(player, platforms, enemies, warp_zones):
    player.update(platforms, enemies, warp_zones)

