from math import sqrt 

class Vector3(object):

    def init (self, x, y, z):

        self.x = x 
        self.y = y 
        self.z = z

    def add (self, x, y, z):

        return Vector3(self.x + x, self.y + y, self.z + z)

    def get_magnitude(self):

        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
