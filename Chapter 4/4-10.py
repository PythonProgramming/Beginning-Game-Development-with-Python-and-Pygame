import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

points = []

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            points.append(event.pos)

    screen.fill((255,255,255))

    if len(points) >= 3:
        pygame.draw.polygon(screen, (0,255,0), points)
    for point in points:
        pygame.draw.circle(screen, (0,0,255), point, 5)

    pygame.display.update()
