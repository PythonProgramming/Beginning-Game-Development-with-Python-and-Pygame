def saturate_color(color): 
    red, green, blue = color 
    red   = min(red, 255)
    green = min(green, 255) 
    blue  = min(blue, 255) 
    return red, green, blue
