import pygame
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2

background_image_filename = 'sushiplate.jpg'
sprite_image_filename = 'fugu.png'

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)
background = pygame.image.load(background_image_filename).convert()
sprite = pygame.image.load(sprite_image_filename).convert_alpha()

clock = pygame.time.Clock()

sprite_pos = Vector2(200, 150)
sprite_speed = 300

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    pressed_keys = pygame.key.get_pressed()

    key_direction = Vector2(0, 0)
    
    if pressed_keys[K_LEFT]:
        key_direction.x = -1
    elif pressed_keys[K_RIGHT]:
         key_direction.x = +1
    if pressed_keys[K_UP]:
        key_direction.y = -1
    elif pressed_keys[K_DOWN]:
        key_direction.y = +1

    key_direction.normalize()

    screen.blit(background, (0,0))
    screen.blit(sprite, (sprite_pos.x,sprite_pos.y))

    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.0

    sprite_pos += key_direction * sprite_speed * time_passed_seconds

    pygame.display.update()
