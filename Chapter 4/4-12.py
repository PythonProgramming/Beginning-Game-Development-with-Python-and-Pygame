import pygame
from pygame.locals import *
from sys import exit 

from random import *

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          exit()

    x, y = pygame.mouse.get_pos() 
    screen.fill((255,255,255)) 
    pygame.draw.ellipse(screen, (0,255,0), (0,0,x,y))

    pygame.display.update()
