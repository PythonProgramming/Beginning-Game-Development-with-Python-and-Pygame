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


