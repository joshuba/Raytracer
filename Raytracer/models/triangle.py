from computergrafik.Blatt2.math.vector import Vector


class Triangle(object):
    def __init__(self, a, b, c, color, reflect):
        self.a = a #point
        self.b = b #point
        self. c = c #point
        self. u = self.b - self.a #direction vector
        self.v = self.c - self.a #direction vector
        self.color = color
        self.reflect = reflect

    def __repr__(self):
        return "Triangle (%s %s)", (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin -self.a
        dv = ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        else:
            wu = w.cross(self.u)
            r = dv.dot(w) / dvu
            s = wu.dot(ray.direction) / dvu
            if 0 <= r and r <= 1 and 0 <= s and s <= 1 and r+s <= 1:
                return wu.dot(self.v) / dvu
            else:
                return None

    def normalAt(self, p):
        return self.u.cross(self.v).normalized()

    def colorAt(self, ray):
        return Vector(self.color[0], self.color[1], self.color[2])