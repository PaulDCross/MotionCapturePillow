import math
import myLibraries.extras

class Vector(object):
    """Vector(x, y)

    Parameters
    ==========
    x   = the x component
    y   = the y component

    Attributes
    ==========
    x   = the x component of this vector determined by the parameter x.
    y   = the y component of this vector determined by the parameter y.
    pos = a list containing the x and y components of this vector.

    Methods
    =======
    add(other)  = returns a Vector object whose x and y components are determined by
                  adding together the x components of this vector and another vector and
                  adding together the y components of this vector and another vector.
    sub(other)  = returns a Vector object whose x and y components are determined by
                  subtracting together the x components of this vector and another vector and
                  subtracting together the y components of this vector and another vector.
    mul(other)  = returns a Vector object whose x and y components are determined by
                  multiplying together the x components of this vector and another vector and
                  multiplying together the y components of this vector and another vector.
    mag         = returns the magnitude of this vector.
    norm        = returns a Vector object which is this vector's unit vector.
    """
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]
        self.pos = [round(self.x, 3), round(self.y, 3)]

    def add(self, vector):
        return Vector([self.x + vector.x, self.y + vector.y])

    def sub(self, vector):
        return Vector([self.x - vector.x, self.y - vector.y])

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def unit(self):
        return Vector([self.x/self.mag(), self.y/self.mag()])

    def mulScalar(self, scalar):
        return Vector([self.x*scalar, self.y*scalar])
