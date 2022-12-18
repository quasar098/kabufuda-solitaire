import pygame
# noinspection PyUnresolvedReferences,PyProtectedMember
from pygame._sdl2 import Window
from constants import *
from utils import *
from game import Game
from solver import solve

# build help for adding assets: https://python.plainenglish.io/packaging-data-files-to-pyinstaller-binaries-6ed63aa20538

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)

loading_image = pygame.image.load(join(dirname(__file__), "assets", "loading.png")).convert_alpha()
screen.blit(loading_image, loading_image.get_rect(center=screen.get_rect().center))
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)

pygame.display.update()
clock = pygame.time.Clock()
game = Game()
last_mp = [0, 0]
last_rel_effect = [0, 0]
init_clicked_on_title = False

pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                solve()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mp()[1] < 83 and mp()[0] < 940:
                    init_clicked_on_title = True
        if event.type == pygame.MOUSEBUTTONUP:
            init_clicked_on_title = False
        # noinspection PyBroadException
        try:
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    if init_clicked_on_title:
                        rel = [mp()[0]-last_mp[0], mp()[1]-last_mp[1]]
                        rel[0] = clamp(rel[0], -40, 40)
                        rel[1] = clamp(rel[1], -40, 40)
                        pgwindow = Window.from_display_module()
                        # noinspection PyUnresolvedReferences
                        pgwindow.position = pgwindow.position[0]+rel[0], pgwindow.position[1]+rel[1]
                        last_rel_effect = rel
        except Exception:
            print("dragging the window is unavailable on this device. please report to the github")
        game.handle_event(event)

    # code here
    game.draw(screen)

    pygame.display.flip()
    clock.tick(FRAMERATE)
    last_mp = list(mp())
    last_mp[0] -= last_rel_effect[0]
    last_mp[1] -= last_rel_effect[1]
