from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

SCREEN_SIZE = (800, 600)

def resize(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glClearColor(1.0, 1.0, 1.0, 0.0)    


def upload_texture(filename, use_alpha=False):
    
    # Read an image file and upload a texture    
    if use_alpha:
        format, gl_format, bits_per_pixel = 'RGBA', GL_RGBA, 4        
    else:
        format, gl_format, bits_per_pixel = 'RGB', GL_RGB, 3
    
    img_surface = pygame.image.load(filename)
    
    #img_surface = premul_surface(img_surface)
    
    data = pygame.image.tostring(img_surface, format, True)    
    
    texture_id = glGenTextures(1)
    
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    
    width, height =  img_surface.get_rect().size
    
    glTexImage2D(   GL_TEXTURE_2D,
                    0,
                    bits_per_pixel,
                    width,
                    height,
                    0,
                    gl_format,
                    GL_UNSIGNED_BYTE,
                    data )
    
    # Return the texture id, so we can use glBindTexture
    return texture_id
    
    
def draw_quad(x, y, z, w, h):
    
    # Send four vertices to draw a quad
    glBegin(GL_QUADS)
    
    glTexCoord2f(0, 0)
    glVertex3f(x-w/2, y-h/2, z)

    glTexCoord2f(1, 0)
    glVertex3f(x+w/2, y-h/2, z)

    glTexCoord2f(1, 1)
    glVertex3f(x+w/2, y+h/2, z)

    glTexCoord2f(0, 1)
    glVertex3f(x-w/2, y+h/2, z)
        
    glEnd()
    

def run():
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
      
    resize(*SCREEN_SIZE)
    init()
       
    # Upload the background and fugu texture
    background_tex = upload_texture('background.png')
    fugu_tex = upload_texture('fugu.png', True)    

    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    # Simple alpha blending
                    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                    glBlendEquation(GL_FUNC_ADD)
                elif event.key == K_2:
                    # Additive alpha blending
                    glBlendFunc(GL_SRC_ALPHA, GL_ONE)                    
                    glBlendEquation(GL_FUNC_ADD)
                elif event.key == K_3:
                    # Subtractive blending
                    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
                    glBlendEquation(GL_FUNC_REVERSE_SUBTRACT)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                                
        # Draw the background
        glBindTexture(GL_TEXTURE_2D, background_tex)
        
        glDisable(GL_BLEND)
        draw_quad(0, 0, -SCREEN_SIZE[1], 600, 600)
        glEnable(GL_BLEND)
        
        # Draw a texture at the mouse position
        glBindTexture(GL_TEXTURE_2D, fugu_tex)
        x, y = pygame.mouse.get_pos()
        x -= SCREEN_SIZE[0]/2
        y -= SCREEN_SIZE[1]/2
        draw_quad(x, -y, -SCREEN_SIZE[1], 256, 256)
        
        pygame.display.flip()
        
    # Free the textures we used
    glDeleteTextures(background_tex)
    glDeleteTextures(fugu_tex)
        
if __name__ == "__main__":
    run()
