import pygame
from pygame.locals import *
from gameobjects.vector3 import Vector3
from math import *
from random import randint

SCREEN_SIZE =  (640, 480)
CUBE_SIZE = 300

def calculate_viewing_distance(fov, screen_width):
    
    d = (screen_width/2.0) / tan(fov/2.0)
    return d
    
    
def run():
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0)
    
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 24)
    
    ball = pygame.image.load("ball.png").convert_alpha()
    
    # The 3D points
    points = []
    
    fov = 90. # Field of view
    viewing_distance = calculate_viewing_distance(radians(fov), SCREEN_SIZE[0])
    
    # Create a list of points along the edge of a cube
    for x in range(0, CUBE_SIZE+1, 20):
        edge_x = x == 0 or x == CUBE_SIZE
        
        for y in range(0, CUBE_SIZE+1, 20):
            edge_y = y == 0 or y == CUBE_SIZE
            
            for z in range(0, CUBE_SIZE+1, 20):
                edge_z = z == 0 or z == CUBE_SIZE
                
                if sum((edge_x, edge_y, edge_z)) >= 2:
                    
                    point_x = float(x) - CUBE_SIZE/2
                    point_y = float(y) - CUBE_SIZE/2
                    point_z = float(z) - CUBE_SIZE/2
                    
                    points.append(Vector3(point_x, point_y, point_z))
    
    # Sort points in z order    
    def point_z(point):
        return point.z
    points.sort(key=point_z, reverse=True)
    
    center_x, center_y = SCREEN_SIZE
    center_x /= 2
    center_y /= 2
    
    ball_w, ball_h = ball.get_size()
    ball_center_x = ball_w / 2
    ball_center_y = ball_h / 2
    
    camera_position = Vector3(0.0, 0.0, -700.)
    camera_speed = Vector3(300.0, 300.0, 300.0)
    
    clock = pygame.time.Clock()
        
    while True:        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
        
        screen.fill((0, 0, 0))
        
        pressed_keys = pygame.key.get_pressed()
        
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.
        
        direction = Vector3()
        if pressed_keys[K_LEFT]:
            direction.x = -1.0
        elif pressed_keys[K_RIGHT]:
            direction.x = +1.0
                        
        if pressed_keys[K_UP]:
            direction.y = +1.0
        elif pressed_keys[K_DOWN]:
            direction.y = -1.0
        
        if pressed_keys[K_q]:
            direction.z = +1.0
        elif pressed_keys[K_a]:
            direction.z = -1.0
            
        if pressed_keys[K_w]:
            fov = min(179., fov+1.)
            w = SCREEN_SIZE[0]
            viewing_distance = calculate_viewing_distance(radians(fov), w)
        elif pressed_keys[K_s]:
            fov = max(1., fov-1.)
            w = SCREEN_SIZE[0]
            viewing_distance = calculate_viewing_distance(radians(fov), w)
        
        camera_position += direction * camera_speed * time_passed_seconds       
        
        # Draw the 3D points
        for point in points:
            
            x, y, z = point - camera_position
            
            if z > 0:
                x =  x * viewing_distance / z
                y = -y * viewing_distance / z
                x += center_x
                y += center_y
                screen.blit(ball, (x-ball_center_x, y-ball_center_y))
           
        # Draw the field of view diagram
        diagram_width = SCREEN_SIZE[0] / 4
        col = (50, 255, 50)
        diagram_points = []
        diagram_points.append( (diagram_width/2, 100+viewing_distance/4) )
        diagram_points.append( (0, 100) )
        diagram_points.append( (diagram_width, 100) )
        diagram_points.append( (diagram_width/2, 100+viewing_distance/4) )
        diagram_points.append( (diagram_width/2, 100) )
        pygame.draw.lines(screen, col, False, diagram_points, 2)        
        
        # Draw the text
        white = (255, 255, 255)
        cam_text = font.render("camera = "+str(camera_position), True, white)        
        screen.blit(cam_text, (5, 5))
        fov_text = font.render("field of view = %i"%int(fov), True, white)
        screen.blit(fov_text, (5, 35))        
        txt = "viewing distance = %.3f"%viewing_distance
        d_text = font.render(txt, True, white)
        screen.blit(d_text, (5, 65))
            
        pygame.display.update()
        
        
if __name__ == "__main__":
    run()
    
    
    
