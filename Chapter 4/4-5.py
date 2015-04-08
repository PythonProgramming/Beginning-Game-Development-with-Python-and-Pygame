def lerp(value1, value2, factor):
    return value1+(value2-value1)*factor

print(lerp(100, 200, 0.))
print(lerp(100, 200, 1.))
print(lerp(100, 200, .5)) 
print(lerp(100, 200, .25))
