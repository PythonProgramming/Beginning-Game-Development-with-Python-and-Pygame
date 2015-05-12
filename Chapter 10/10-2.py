tank.explode() # Do explosion visual 
explosion_channel = explosion_sound.play() 
if explosion_channel is not None:
    left, right = stereo_pan(tank.position.x, SCREEN_SIZE[0])
    explosion_channel.set_volume(left, right)
