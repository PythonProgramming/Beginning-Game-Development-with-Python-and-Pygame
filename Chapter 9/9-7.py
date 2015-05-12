# Create a display list 
tank_display_list = glGenLists(1) 
glNewList(tank_display_list, GL_COMPILE)

draw_tank()

# End the display list 
glEndList()
