def stereo_pan(x_coord, screen_width):

    right_volume = float(x_coord) / screen_width 
    left_volume = 1.0 - right_volume

    return (left_volume, right_volume)
