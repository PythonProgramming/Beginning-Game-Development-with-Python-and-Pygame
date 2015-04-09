import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

# Get a list of joystick objects
joysticks = []
for joystick_no in range(pygame.joystick.get_count()):
    stick = pygame.joystick.Joystick(joystick_no)
    stick.init()
    joysticks.append(stick)

if not joysticks:
    print("Sorry! No joystick(s) to test.")
    pygame.quit()
    exit()

active_joystick = 0


pygame.display.set_caption(joysticks[0].get_name())

def draw_axis(surface, x, y, axis_x, axis_y, size):

    line_col = (128, 128, 128)
    num_lines = 40
    step = size / float(num_lines)
    for n in range(num_lines):
        line_col = [(192, 192, 192), (220, 220, 220)][n&1]
        pygame.draw.line(surface, line_col, (x+n*step, y), (x+n*step, y+size))
        pygame.draw.line(surface, line_col, (x, y+n*step), (x+size, y+n*step))

    pygame.draw.line(surface, (0, 0, 0), (x, y+size/2), (x+size, y+size/2))
    pygame.draw.line(surface, (0, 0, 0), (x+size/2, y), (x+size/2, y+size))

    draw_x = int(x + (axis_x * size + size) / 2.)
    draw_y = int(y + (axis_y * size + size) / 2.)
    draw_pos = (draw_x, draw_y)
    center_pos = (x+size/2, y+size/2)
    pygame.draw.line(surface, (0, 0, 0), center_pos, draw_pos, 5)
    pygame.draw.circle(surface, (0, 0, 255), draw_pos, 10)


def draw_dpad(surface, x, y, axis_x, axis_y):

    col = (255, 0, 0)
    if axis_x == -1:
        pygame.draw.circle(surface, col, (x-20, y), 10)
    elif axis_x == +1:
       pygame.draw.circle(surface, col, (x+20, y), 10)

    if axis_y == -1:
        pygame.draw.circle(surface, col, (x, y+20), 10)
    elif axis_y == +1:
        pygame.draw.circle(surface, col, (x, y-20), 10)

while True:

    joystick = joysticks[active_joystick]

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if event.type == KEYDOWN:
        if event.key >= K_0 and event.key <= K_1:
            num = event.key - K_0
     
            if num < len(joysticks):
                active_joystick = num
                name = joysticks[active_joystick].get_name()
                pygame.display.set_caption(name)

    # Get a list of all the axis
    axes = []
    for axis_no in range(joystick.get_numaxes()):
        axes.append( joystick.get_axis(axis_no) )

    axis_size = min(256, 640 / (joystick.get_numaxes()/2))

    pygame.draw.rect(screen, (255, 255,255), (0, 0, 640, 480))

    # Draw all the axes (analog sticks)
    x = 0
    for axis_no in range(0, len(axes), 2):
        axis_x = axes[axis_no]
        if axis_no+1 < len(axes):
            axis_y = axes[axis_no+1]
        else:
            axis_y = 0.
        draw_axis(screen, x, 0, axis_x, axis_y, axis_size)
        x += axis_size


    # Draw all the hats (d-pads)
    x, y = 50, 300
    for hat_no in range(joystick.get_numhats()):
        axis_x, axis_y = joystick.get_hat(hat_no)
        draw_dpad(screen, x, y, axis_x, axis_y)
        x+= 100


    #Draw all the buttons x, y = 0.0, 390.0
    button_width = 640 / joystick.get_numbuttons()
    for button_no in range(joystick.get_numbuttons()):
        if joystick.get_button(button_no):
            pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), 20)
        x += button_width

    pygame.display.update()
