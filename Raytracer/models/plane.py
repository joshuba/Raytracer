from computergrafik.Blatt2.math.vector import Vector


class Plane(object):
    def __init__(self, point, normal, color, reflect, chess):
        self.point = point #point
        self.normal = normal #vector
        self.color = color
        self.reflect = reflect
        self.chess = chess

        self.otherColor = Vector(0, 0, 0)
        self.checkSize = 6


    def __repr__(self):
        return "Plane (%s %s)", (repr(self.point), repr(self.normal))

    def normalAt(self, p):
        return self.normal

    def intersectionParameter(self, ray):
        op = ray.origin - self.point
        assert(type(op) is Vector)
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b:
            return -a/b #SP
        else:
            return None #parallel zur ebene

    def colorAt(self, p):
        "Schachbrettmuster"
        if self.chess:
            v = Vector(p.x, p.y, p.z)
            v = v.scale(1.0 / self.checkSize)
            if (int(abs(v.x)+0.5) + int(abs(v.y) +0.5) + int(abs(v.z) + 0.5)) % 2:
                return self.otherColor
        return Vector(self.color[0], self.color[1], self.color[2])
