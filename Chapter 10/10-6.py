import pygame
from pygame.locals import *

from math import sqrt
import os
import os.path

# Location of music on your computer
MUSIC_PATH = "./MUSIC"
SCREEN_SIZE = (800, 600)

def get_music(path):
    
    # Get the filenames in a folder
    raw_filenames = os.listdir(path)
    
    music_files = []
    for filename in raw_filenames:
                
        # We only want ogg files
        if filename.endswith('.ogg'):
            music_files.append(os.path.join(MUSIC_PATH, filename))
            
    return sorted(music_files)


class Button(object):
    
    def __init__(self, image_filename, position):
        
        self.position = position
        self.image = pygame.image.load(image_filename)

    def render(self, surface):
        
        # Render at the center
        x, y = self.position
        w, h = self.image.get_size()
        x -= w /2
        y -= h / 2
        
        surface.blit(self.image, (x, y))
        
        
    def is_over(self, point):
        
        # Return True if a point is over the button
        point_x, point_y = point
        x, y = self.position
        w, h = self.image.get_size()
        x -= w /2
        y -= h / 2
        
        in_x = point_x >= x and point_x < x + w
        in_y = point_y >= y and point_y < y + h
            
        return in_x and in_y

def run():
        
    pygame.mixer.pre_init(44100, 16, 2, 1024*4)
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0)     
    
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont("default_font", 50, False)    
    
    # Create our buttons
    x = 100
    y = 240
    button_width = 150
    
    # Store the buttons in a dictionary, so we can assign them names
    buttons = {}
    buttons["prev"] = Button("prev.png", (x, y))    
    buttons["pause"] = Button("pause.png", (x+button_width*1, y))
    buttons["stop"] = Button("stop.png", (x+button_width*2, y))
    buttons["play"] = Button("play.png", (x+button_width*3, y))
    buttons["next"] = Button("next.png", (x+button_width*4, y))
            
    music_filenames = get_music(MUSIC_PATH)
    
    if len(music_filenames) == 0:
        print("No OGG files found in ", MUSIC_PATH)
        return
    
    white = (255, 255, 255)    
    label_surfaces = []    
    
    # Render the track names
    for filename in music_filenames:
        
        txt = os.path.split(filename)[-1]
        
        print("Track:", txt)
        
        txt = txt.split('.')[0]
        surface = font.render(txt, True, (100, 0, 100))
        label_surfaces.append(surface)
        
    current_track = 0
    max_tracks = len(music_filenames)
    
    pygame.mixer.music.load( music_filenames[current_track] )  
    
    clock = pygame.time.Clock()
        
    playing = False
    paused = False
    
    # This event is sent when a music track ends
    TRACK_END = USEREVENT + 1
    pygame.mixer.music.set_endevent(TRACK_END)
        
    while True:
        
        button_pressed = None
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                quit()
            
            if event.type == MOUSEBUTTONDOWN:
                
                # Find the pressed button
                for button_name, button in buttons.items():
                    if button.is_over(event.pos):
                        print(button_name, "pressed")
                        button_pressed = button_name
                        break
            
            if event.type == TRACK_END:
                # If the track has ended, simulate pressing the next button
                button_pressed = "next"
        
        if button_pressed is not None:
                        
            if button_pressed == "next":
                current_track = (current_track + 1) % max_tracks
                pygame.mixer.music.load( music_filenames[current_track] )
                if playing:
                    pygame.mixer.music.play()
                
            elif button_pressed == "prev":
                
                # If the track has been playing for more that 3 seconds,
                # rewind i, otherwise select the previous track
                if pygame.mixer.music.get_pos() > 3000:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play()                                        
                else:
                    current_track = (current_track - 1) % max_tracks
                    pygame.mixer.music.load( music_filenames[current_track] )
                    if playing:
                        pygame.mixer.music.play()
                
            elif button_pressed == "pause":
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:                    
                    pygame.mixer.music.pause()
                    paused = True
                
            elif button_pressed == "stop":                
                pygame.mixer.music.stop()
                playing = False
                
            elif button_pressed == "play":
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    if not playing:
                        pygame.mixer.music.play()
                        playing = True
                        
        
        screen.fill(white)
        
                
        # Render the name of the currently track
        label = label_surfaces[current_track]
        w, h = label.get_size()
        screen_w = SCREEN_SIZE[0]        
        screen.blit(label, ((screen_w - w)/2, 450))
        
        # Render all the buttons
        for button in list(buttons.values()):
            button.render(screen)
        
        # No animation, 5 frames per second is fine!
        clock.tick(5)
        pygame.display.update()


if __name__ == "__main__":
            
    run()
