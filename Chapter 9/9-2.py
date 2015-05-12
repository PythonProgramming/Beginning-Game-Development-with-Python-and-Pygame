#pseudocode
tank_heading = Vector3(tank_matrix.forward)
tank_matrix.translation += tank_heading * tank_speed * time_passed
