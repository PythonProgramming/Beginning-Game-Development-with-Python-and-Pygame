from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

screen = pygame.display.set_mode((640, 480), HWSURFACE|DOUBLEBUF|OPENGL)

def resize(width, height):
    glViewport(0, 0, width, height) 
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity()
    gluPerspective(60, float(width)/height, 1, 10000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():

    glEnable(GL_DEPTH_TEST)
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glShadeModel(GL_FLAT)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSITION, (0, 1, 1, 0))
