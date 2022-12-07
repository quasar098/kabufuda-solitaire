import pygame
from constants import *
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)
from utils import *
from card import Card
from stack import Stack

clock = pygame.time.Clock()
stacks = [
    Stack(46, 223, [Card(0, 0, 3), Card(0, 0, 1), Card(0, 0, 1)]),
    Stack(174, 223, []),
    Stack(128*1+174, 233, []),
    Stack(128*2+174, 233, []),
    Stack(128*3+174, 233, []),
    Stack(128*4+174, 233, []),
    Stack(128*6+174, 233, []),
    Stack(128*5+174, 233, [])
]

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        for stack in stacks:
            grabbed = [card for card in stack.cards if card.grabbed]
            handled = stack.handle_event(event)
            if handled:
                print(handled.grabbed)

    # code here
    screen.blit(BACKBOARD_TOP, (0, 0))
    screen.blit(BACKBOARD_MAIN, (0, 202))
    for stack in stacks:
        stack.draw(screen)

    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()
