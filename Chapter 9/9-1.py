from gameobjects.matrix44 import *

identity = Matrix44()
print(identity)
p1 = (1.0, 2.0, 3.0)
identity.transform(p1)

assert identity.get_column(3) == (0, 0, 0, 1), "Something is wrong with this matrix!"
