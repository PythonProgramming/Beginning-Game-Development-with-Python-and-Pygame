from math import log, ceil
def next_power_of_2(size):
    return 2 ** ceil(log(size, 2))
