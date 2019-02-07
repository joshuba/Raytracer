#!user/bin/python3
import numpy as np

class Vector(object):

    def __init__(self, x, y, z):
        self.coords = np.array([x, y, z])
        self.x = x
        self.y = y
        self.z = z


    def __repr__(self):
        return "V (%s  %s  %s)" % (self.x, self.y, self.z)

    def __str__(self):
        return "V (%s  %s  %s)" % (self.x, self.y, self.z)

    def __add__(self, other):
        a = np.add(self.coords, other.coords)
        return Vector(a[0], a[1], a[2])

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.dot(other)
        else:
            return self.scale(other)


    def length(self):
        return(np.sqrt(self.x**2 + self.y**2 + self.z**2))

    def scale(self, s):
        n = self.coords *s
        return Vector(n[0], n[1], n[2])

    def dot(self, vector):
        n = np.dot(self.coords, vector.coords)
        return n

    def cross(self, vector):
        a = np.cross(self.coords, vector.coords)

        return Vector(a[0], a[1], a[2])

    def normalized(self):
        return self.scale(1/self.length())

    def lenght(self):
        return np.math.sqrt(self.x++2 + self.y++2 + self.z++2)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


