def get_attenuation(distance, constant, linear, quadratic):
    return 1.0 / (constant + linear * distance + quadratic * (distance ** 2))
