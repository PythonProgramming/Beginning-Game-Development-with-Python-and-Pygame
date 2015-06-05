from math import radians

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

SCREEN_SIZE = (800, 600)

def resize(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():

    glEnable(GL_TEXTURE_2D)
    glClearColor(1.0, 1.0, 1.0, 0.0)

def run():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

    resize(*SCREEN_SIZE)
    init()

    # Load the textures
    texture_surface = pygame.image.load("sushitex.png")
    # Retrieve the texture data
    texture_data = pygame.image.tostring(texture_surface, 'RGB', True)

    # Generate a texture id
    texture_id = glGenTextures(1)
    # Tell OpenGL we will be using this texture id for texture operations
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Tell OpenGL how to scale images
    glTexParameteri(GL_TEXTURE_2D,  GL_TEXTURE_MAG_FILTER, GL_LINEAR) 
    glTexParameteri(GL_TEXTURE_2D,  GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    # Tell OpenGL that data is aligned to byte boundries
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    # Get the dimensions of the image
    width, height = texture_surface.get_rect().size


    gluBuild2DMipmaps( GL_TEXTURE_2D, 
                   3, 
                   width, 
                   height, 
                   GL_RGB, 
                   GL_UNSIGNED_BYTE, 
                   texture_data )


    clock = pygame.time.Clock()

    tex_rotation = 0.0

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()


        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.
        tex_rotation += time_passed_seconds * 360.0 / 8.0


        # Clear the screen (similar to fill)
        glClear(GL_COLOR_BUFFER_BIT)

        # Clear the model-view matrix
        glLoadIdentity()

        # Set the modelview matrix
        glTranslatef(0.0, 0.0, -600.0)
        glRotate(tex_rotation, 1, 0, 0)

        # Draw a quad (4 vertices, 4 texture coords)
        glBegin(GL_QUADS)

        glTexCoord2f(0, 1)
        glVertex3f(-300, 300, 0)

        glTexCoord2f(1, 1)
        glVertex3f(300, 300, 0)

        glTexCoord2f(1, 0)
        glVertex3f(300, -300, 0)

        glTexCoord2f(0, 0)
        glVertex3f(-300, -300, 0)

        glEnd()

        pygame.display.flip()

    glDeleteTextures(texture_id)

if __name__ == "__main__":
    run()
