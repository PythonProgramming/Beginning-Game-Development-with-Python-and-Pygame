from math import radians

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

# Import the Model3D class
import model3d

SCREEN_SIZE = (800, 600)

def resize(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():

    # Enable the GL features we will be using
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)

    glShadeModel(GL_SMOOTH)
    glClearColor(1.0, 1.0, 1.0, 0.0) # white

    # Set the material
    glMaterial(GL_FRONT, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    glMaterial(GL_FRONT, GL_DIFFUSE, (0.2, 0.2, 0.2, 1.0))
    glMaterial(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterial(GL_FRONT, GL_SHININESS, 10.0)

    # Set light parameters
    glLight(GL_LIGHT0, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    glLight(GL_LIGHT0, GL_DIFFUSE, (0.4, 0.4, 0.4, 1.0))
    glLight(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    # Enable light 1 and set position
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSITION,  (0, .5, 1, 0))


def run():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

    resize(*SCREEN_SIZE)
    init()

    clock = pygame.time.Clock()

    # Read the model
    tank_model = model3d.Model3D()
    tank_model.read_obj('mytank.obj')

    rotation = 0.0

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0

        glLoadIdentity()
        glRotatef(15, 1, 0, 0)
        glTranslatef(0.0, -1.5, -3.5)

        rotation += time_passed_seconds * 45.0
        glRotatef(rotation, 0, 1, 0)

        tank_model.draw_quick()

        pygame.display.flip()
            

if __name__ == "__main__":
    run()
