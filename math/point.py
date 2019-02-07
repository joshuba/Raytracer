#!user/bin/python3
import numpy

from computergrafik.Blatt2.math.vector import Vector



class Point(object):

    def __init__(self, x, y, z):
        self.coords = numpy.array([x, y, z])
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "P (%s  %s  %s)" % (self.x, self.y, self.z)

    def __str__(self):
        return "P (%s  %s  %s)" % (self.x, self.y, self.z)

    def __sub__(self, other):
        if type(other) is Point:
            before = self.coords
            other = other.coords
            lst = before - other

            return Vector(lst[0], lst[1], lst[2])

    def __add__(self, other):
        x, y, z = numpy.add(self.coords, other.coords)
        if isinstance(other, Vector):
            return Point(x, y, z)
