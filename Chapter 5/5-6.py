class Vector2:
    
    def __init__(self, x=0, y=0):        
        self.x = x
        self.y = y
        
    def __str__(self):
        return "(%s, %s)"%(self.x, self.y)
        
    def from_points(P1, P2):

        # ( P2[0] - P1[0], P2[1] - P1[1] ) is the same as:
        # numpy.array(P1) - numpy.array(P1)
        
        return Vector2(P2[0] - P1[0], P2[1] - P1[1])
