import math
from computergrafik.Blatt2.math.vector import Vector


class Sphere(object):
    def __init__(self, center, radius, color, reflect):
        self.center = center #point
        self.radius = radius #scalar
        self.color = color
        self.reflect = reflect

    def __repr__(self):
        return "Sphere (%s %s)" % (repr(self.center), repr(self.radius))

    def intersectionParameter(self, ray):
        co = self.center - ray.origin #vector
        v = co.dot(ray.direction) #<co,d>
        discriminant = v*v - co.dot(co) + self.radius*self.radius
        if discriminant <= 0: #kein Schnittpunkt
            return None
        else: #Schnittpunkt
            return v - math.sqrt(discriminant) #parameter t

    def normalAt(self, p):
        return (p -self.center).normalized()

    def colorAt(self, ray):
        return Vector(self.color[0], self.color[1], self.color[2])



