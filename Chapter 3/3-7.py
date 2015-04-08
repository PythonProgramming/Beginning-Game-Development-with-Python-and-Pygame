import pygame 
from pygame.locals import * 
from sys import exit

background_image_filename = 'sushiplate.jpg'  
SCREEN_SIZE = (640, 480) 
message="    This is a demonstration of the scrolly message script. " 
 
pygame.init() 
screen = pygame.display.set_mode(SCREEN_SIZE) 
 
font = pygame.font.SysFont("arial", 80); 
text_surface = font.render(message, True, (0, 0, 255)) 
 
x = 0 
y = ( SCREEN_SIZE[1] - text_surface.get_height() ) / 2 
 
background = pygame.image.load(background_image_filename).convert() 
 
while True: 
 
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            exit() 
 
    screen.blit(background, (0,0)) 
 
    x-= 2 
    if x < -text_surface.get_width(): 
        x = 0 
 
    screen.blit(text_surface, (x, y)) 
    screen.blit(text_surface, (x+text_surface.get_width(), y)) 
    pygame.display.update() 
