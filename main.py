import pygame
# noinspection PyUnresolvedReferences
from pygame._sdl2 import Window
from constants import *
from utils import *
from game import Game

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)
screen.fill((255, 255, 0))
pygame.display.update()
clock = pygame.time.Clock()
game = Game()
last_mp = [0, 0]
last_rel_effect = [0, 0]

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                if mp()[1] < 83 and mp()[0] < 1000:
                    rel = [mp()[0]-last_mp[0], mp()[1]-last_mp[1]]
                    rel[0] = clamp(rel[0], -40, 40)
                    rel[1] = clamp(rel[1], -40, 40)
                    pgwindow = Window.from_display_module()
                    pgwindow.position = pgwindow.position[0]+rel[0], pgwindow.position[1]+rel[1]
                    last_rel_effect = rel
        game.handle_event(event)

    # code here
    game.draw(screen)

    pygame.display.flip()
    clock.tick(FRAMERATE)
    last_mp = list(mp())
    last_mp[0] -= last_rel_effect[0]
    last_mp[1] -= last_rel_effect[1]
