from gameobjects.vector3 import *

A = Vector3(6, 8, 12)
B = Vector3(10, 16, 12)

print("A is", A)
print("B is", B)
print("Magnitude of A is", A.get_magnitude())
print("A+B is", A+B)
print("A-B is", A-B)


print("A normalized is", A.get_normalized())
print("A*2 is", A * 2)
