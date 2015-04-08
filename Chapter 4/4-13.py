import pygame
from pygame.locals import *
from sys import exit

from random import *
from math import pi

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    x, y  = pygame.mouse.get_pos() 
    angle = (x/639.)*pi*2. 
    screen.fill((255,255,255))
    pygame.draw.arc(screen, (0,0,0), (0,0,639,479), 0, angle)

    pygame.display.update()
