import math
from PIL import Image

from computergrafik.Blatt2.Raytracer.ray import Ray
from computergrafik.Blatt2.math.point import Point
from computergrafik.Blatt2.math.vector import Vector

BACKGROUND_COLOR = (0, 0, 0)
MAXRECLEVEL = 0
REFLECTION = 0.3
SCHATTEN = True
KA = 0.4
KD = 0.5 #verteilt das licht gleichmäßig in alle richtungen
KS = 0.5
CA = Vector(50, 50, 50)




class Camera(object):
    def __init__(self, fieldOfView, aspectRatio, e: Point, c: Point, up: Vector, objectList, sonne: Point):
        "Kameraobjekt"


        self.fieldOfView = fieldOfView
        self. aspectRatio = aspectRatio
        self.e = e #ursprung
        self.c = c #center
        self. up = up
        self.sonne = sonne #point
        self.objectList = objectList


        #Erstelle Euklid. SzenenKoordinatensystem
        self.f = (c - e).normalized() #normierter vektor
        self.s = self.f.cross(up).normalized()
        self.u = self.s.cross(self.f)


    def takeAPicture(self, pictureWidth, pictureHeight):
        "Zentrale Raytracingmethode"
        pro = pictureWidth / 10 #zur berechnung des Fortschritts

        img = Image.new('RGB', (pictureWidth, pictureHeight), "black")
        pixels = img.load() #create the pixel map


        #Berechne größe der Szene
        self.height = 2 * math.tan(self.fieldOfView/2)
        self.width = self.aspectRatio * self.height


        #Berechne Pixelgroesse
        self.pixelWidth = self.width / (pictureWidth - 1)
        self.pixelHeight = self.height / (pictureHeight - 1)


        #Iteriere durch jeden Pixel des Bildes und erstelle einen Strahl
        for x in range(pictureWidth):
            for y in range(pictureHeight):
                ray = self.createRay(x, y)
                color = self.traceRay(0, ray) #berechne Farbe

                pixels[pictureWidth - 1 -x, pictureHeight - 1 - y] = tuple(color)
            if x % pro == 0:
                print((str((x/pictureWidth)*100)) + "%")

        img.show()


    def createRay(self, x, y):
        "Erstelle Strahl anhand der aktuellen Pixelinformationen"
        xcomp = self.s.scale(x * self.pixelWidth - self.width/ 2)
        ycomp = self.u.scale(y * self.pixelHeight - self.height/ 2)
        r = Ray(self.e, (self.f + xcomp) + ycomp)
        return r


    def traceRay(self, level, ray):
        "Verfolgt den Strahl und berechnet Schnittpunkt"
        hitPointData = self.intersect(ray) #Schnittpunkt des PixelStrahls
        if level == MAXRECLEVEL:
            return BACKGROUND_COLOR
        if hitPointData:
            return self.shade(level, hitPointData) #berechne Farbe des Pixels anhand des Schnittpunktes
        return BACKGROUND_COLOR #Ansonsten färbe in Hintergrundfarbe


    def intersect(self, ray):
        "Berechne Schnittpunkt des Strahls mit allen Objekten"
        maxdist = float('inf')
        aktobj = None
        schatten = None
        sp = None

        #Prüfe jedes Objekt, ob es einen Schnittpunkt gibt
        for o in self.objectList:
            hitdist = o.intersectionParameter(ray)

            #Falls es einen Schnittpunkt gibt
            if hitdist and 0 < hitdist < maxdist:
                maxdist = hitdist #nehme den vordersten Schnittpunkt
                sp = ray.origin + ray.direction.scale(maxdist) #berechne Schnittpunkt
                aktobj = o

        # Wird pixel von einem Schatten getroffen?
        if aktobj:  #wenn es einen schnittpunkt gegeben hat
            if self.checkschatten(sp):
                schatten = True

        if aktobj == None:
            return None #kein schnittpunkt
        return sp, maxdist, ray, aktobj, schatten  #berechne Schnittpunkt


    def computeReflectedRay(self, hitPointData):
        "Einfallswinkel = Ausfallswinkel, berechne reflektierten Strahl"
        sp = hitPointData[0]
        d = hitPointData[2].direction
        n = hitPointData[3].normalAt(sp)
        dr = d + n.scale(n.dot(d) * 2 * (-1))
        return Ray(sp, dr)


    def shade(self, level, hitPointData):
        "Berechnet die Farbe eines Pixels anhand der Schnittpunktinformationen, gegebenfalls Rekursiv"
        directColor = self.phong(hitPointData)

        resultcolor = directColor #als Vektor
        reflectedRay = self.computeReflectedRay(hitPointData)


        if hitPointData[3].reflect: #falls Objekt reflektieren soll
            reflectedColor = self.traceRay(level + 1, reflectedRay) #rekursionsaufruf

            directColor = directColor.scale(1-REFLECTION) #vector
            reflectedColor = Vector(reflectedColor[0], reflectedColor[1], reflectedColor[2]).scale(REFLECTION) #vector
            resultcolor = directColor + reflectedColor #überschreibe Farbe mit Reflektionsfarbe

        resultcolor = tuple(map(self.normalize, resultcolor)) #erstelle Tupel aus Vektor


        if hitPointData[4]:  # wenn ein Schatten auf dem Pixel liegt
            t = (int(resultcolor[0]*0.6), int(resultcolor[1]*0.6), int(resultcolor[2]*0.6)) #farbwert abdunkeln
            resultcolor = t
        return resultcolor



    def checkschatten(self, sp):
        "Prüfe, ob der Schnittpunkt im Schatten eines anderen Objektes liegt"
        if SCHATTEN is False:
            return False

        for o in self.objectList:
            isp = o.intersectionParameter(Ray(sp, self.sonne - sp))

            if isp and isp > 0.001:
                return True
                break


    def normalize(self, x):
        "Fange zu hohe oder niedrige Farbwerte ab"
        if x > 255:
            return 255
        elif x < 0:
            return 0
        else:
            return int(x)


    def phong(self, hitPointData):
        "Berechnung der Farben nach Phong"
        sp = hitPointData[0]
        ray = hitPointData[2]
        obj = hitPointData[3]

        ka = KA
        kd = KD #verteilt das licht gleichmäßig in alle richtungen
        ks = KS
        ca = CA
        d = ray.direction.normalized()
        l = (self.sonne - sp).normalized()
        n = obj.normalAt(sp).normalized()
        cin = obj.colorAt(sp)
        lr = (l + (n.scale((l.dot(n) * 2))).scale(-1)).normalized()

        amb = ca.scale(ka)
        dif = cin.scale(l.dot(n) * kd)
        spek = cin * ks * (lr.dot(n))**2

        color = amb + dif + spek

        return color












