import math

from computergrafik.Blatt2.Raytracer.camera import Camera
from computergrafik.Blatt2.Raytracer.models.plane import Plane
from computergrafik.Blatt2.Raytracer.models.sphere import Sphere
from computergrafik.Blatt2.Raytracer.models.triangle import Triangle
from computergrafik.Blatt2.math.point import Point
from computergrafik.Blatt2.math.vector import Vector

def main():
    objects = []


    sonne = Point(30, 0, 10)

    ebene1 = Plane(Point(0, 0, -7), Vector(0, 0, 1), (255,255,255), False, True) #parralel zur kamera

    kugel1 = Sphere(Point(40, 0, 1), 2, (255,0,0), True)  # hoehe, drehen, hinter, größe
    kugel2 = Sphere(Point(40, 3, -2), 2, (0,255,0), True)  # hoehe, drehen, hinter, größe
    kugel3 = Sphere(Point(40, -3, -2), 2, (0,0,255), True)  # hoehe, drehen, hinter, größe

    dreieck1 = Triangle(Point(40, 3, -2), Point(40, -3, -2), Point(40, 0, 1), (255, 255, 0), False)


    objects.append(ebene1)
    objects.append(kugel1)
    objects.append(kugel2)
    objects.append(kugel3)
    objects.append(dreieck1)


    # Definiere Kamera / Koordinatensystem
    e = Point(0, 0, 0)
    c = Point(1, 0, 0)
    up = Vector(0, 0, 1)
    angle = math.pi/8



    cam = Camera(angle, 1/1, e, c, up, objects, sonne)
    cam.takeAPicture(300 , 300)

def Algebratest():
    v1 = Vector(12, 5, 11)
    v2 = Vector(33, 6, 1)
    print(v1 + v2)


main()
