
"""
Sphere.py
Clase Sphere usada en RayTracer
"""
from Render import color, V3, V4
from linearAlgebra import *
from numpy import arccos, arctan2
from Intersect import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

WHITE = color(1,1,1)

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, direction):
        L = restarVectores(self.center, orig)
        tca = dot(L, direction)
        l = norma(L) # magnitud de L
        d = (l**2 - tca**2) ** 0.5
        if d > self.radius:
            return None

        # thc es la distancia de P1 al punto perpendicular al centro
        thc = (self.radius ** 2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1

        if t0 < 0: # t0 tiene el valor de t1
            return None

        # P = O + tD
        me = multiplicarPorEscalar(t0 , direction)
        hit = sumarVectores(orig, me)
        norm = restarVectores( hit, self.center )
        norm = normalizado(norm) 

        u = 1 - (arctan2( norm[2], norm[0]) / (2 * pi) + 0.5)
        v =  arccos(-norm[1]) / pi

        uvs = [u, v]


        return Intersect(distance = t0,
                         point = hit,
                         normal = norm,
                         texCoords = uvs,
                         sceneObject = self)

