import sys

import numpy as np
import pygame
from pygame.locals import *

pygame.init()


class Firefly(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([2, 2])
        self.image.fill(color)
        self.rect = self.image.get_rect()


def draw_fireflies(screen: pygame.Surface, flies):
    """Blits fireflies on the given surface and returns the rectangles on which it was drawn
    """
    fnb = Firefly((255, 0, 0))
    fb = Firefly((255, 255, 0))
    for fly in flies.T:
        # print(fly)
        f = fb if fly[2] < 3 else fnb
        f.rect.center = tuple(fly[:2])
        screen.blit(f.image, f.rect)


def update_fireflies(flies: np.ndarray):
    print(fireflies[:, 0])
    flies[:, 2] += 5 * (np.random.random(flies[:, 2].shape) - 0.5)
    flies[0] %= W
    flies[1] %= H
    flies[2] = (flies[2] + 1) % 12
    return flies


W, H = 500, 300
DISPLAYSURF = pygame.display.set_mode((W, H), pygame.RESIZABLE)
FPS = pygame.time.Clock()

N = 100
fireflies = np.random.random((3, N))
fireflies[0] *= W
fireflies[1] *= H
fireflies[2] = np.round(10 * fireflies[2])
print(fireflies[2])

while True:
    DISPLAYSURF.fill((0, 0, 0))
    draw_fireflies(DISPLAYSURF, fireflies)
    fireflies = update_fireflies(fireflies)
    pygame.display.update()
    FPS.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
