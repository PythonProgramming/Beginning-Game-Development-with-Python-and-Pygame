def scale_color(color, scale): 
    red, green, blue = color 
    red   = int(red*scale)
    green = int(green*scale) 
    blue  = int(blue*scale) 
    return red, green, blue

fireball_orange = (221, 99, 20)
print(fireball_orange)
print(scale_color(fireball_orange, .5))
