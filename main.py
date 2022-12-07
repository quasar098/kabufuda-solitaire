import pygame
from constants import *
from utils import *
from game import Game

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)
clock = pygame.time.Clock()
game = Game()

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        game.handle_event(event)

    # code here
    game.draw(screen)

    pygame.display.flip()
    clock.tick(FRAMERATE)
