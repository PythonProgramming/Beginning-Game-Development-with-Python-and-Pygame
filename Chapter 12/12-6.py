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
    glEnable(GL_TEXTURE_2D)
    glShadeModel(GL_SMOOTH)

    # Enable light 1 and set position
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSITION,  (0, .5, 1))


def run():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN|HWSURFACE|OPENGL|DOUBLEBUF)

    resize(*SCREEN_SIZE)
    init()    
    
    # Read the skybox model
    sky_box = model3d.Model3D()
    sky_box.read_obj('tanksky/skybox.obj')        
    
    # Set the wraping mode of all textures in the sky-box to GL_CLAMP_TO_EDGE
    for material in sky_box.materials.values():
        
        glBindTexture(GL_TEXTURE_2D, material.texture_id)    
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)        

    
    # Used to rotate the world
    mouse_x = 0.0
    mouse_y = 0.0    
    
    #Don't display the mouse cursor
    pygame.mouse.set_visible(False)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                pygame.quit()
                quit()

        # We don't need to clear the color buffer (GL_COLOR_BUFFER_BIT)
        # because the skybox covers the entire screen 
        glClear(GL_DEPTH_BUFFER_BIT)        

        glLoadIdentity()                        

        mouse_rel_x, mouse_rel_y = pygame.mouse.get_rel()
        mouse_x += float(mouse_rel_x) / 5.0
        mouse_y += float(mouse_rel_y) / 5.0
                
        # Rotate around the x and y axes to create a mouse-look camera
        glRotatef(mouse_y, 1, 0, 0)
        glRotatef(mouse_x, 0, 1, 0)        

        # Disable lighting and depth test
        glDisable(GL_LIGHTING)
        glDepthMask(False)
        
        # Draw the skybox
        sky_box.draw_quick()
        
        # Re-enable lighting and depth test before we redraw the world
        glEnable(GL_LIGHTING)
        glDepthMask(True)        
        
        # Here is where we would draw the rest of the world in a game

        pygame.display.flip()

if __name__ == "__main__":
    run()


