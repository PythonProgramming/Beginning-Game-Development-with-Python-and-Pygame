from math import tan

def calculate_viewing_distance(fov, screen_width):

    d = (screen_width/2.0) / tan(fov/2.0)
    return d
