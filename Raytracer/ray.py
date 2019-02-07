

class Ray(object):
    "Strahlenklasse"

    def __init__(self, origin, direction):
        self.origin = origin #point
        self.direction = direction.normalized() #normierter vector

    def __repr__(self):
        return "Ray(%s, %s)" %(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)
