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
        if event.type == MOUSEMOTION: 
           points.append(event.pos) 
           if len(points)>100:
               del points[0]

    screen.fill((255, 255, 255))

    if len(points)>1:
        pygame.draw.lines(screen, (0,255,0), False, points, 2)

    pygame.display.update()
